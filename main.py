from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import User
from database.postgresql import PostgreSQLDatabase
import config as cnf
import keyboard
import logging
import base
import sys, os

env = sys.argv[1]

if env == "dev":
    config = cnf.DevelopmentConfig
else:
    config = cnf.ProductionConfig

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
dp.filters_factory.bind(base.IsOwner)

i18n = I18nMiddleware('base', 'locale')
dp.middleware.setup(i18n)

_ = i18n.gettext

pg = PostgreSQLDatabase(os.getenv("DATABASE_URL"))


@dp.message_handler(commands=["start"])
async def startMessage(message: types.Message):
    if not pg.getUser(message.from_user):
        pg.addUser(message.from_user)

    await message.answer(_(base.START_MESSAGE_TEXT), reply_markup=keyboard.startMarkup())

@dp.message_handler(commands=["help"])
async def helpMessage(message: types.Message):

    await message.reply(_(base.HELP_MESSAGE_TEXT))
    return

@dp.message_handler(commands=["lang"])
async def langMessage(message: types.Message):
    if message.get_args() and message.get_args() in cnf.BotConfig.locales:
        pg.setUserLocale(message.from_user, message.get_args()[0])
        return


@dp.message_handler(commands=["change"], is_owner=True, is_reply=True)
async def changeTableMessage(message: types.Message, state: FSMContext):
    reply_to_message = message.reply_to_message.text.lower()
    classroom, weekday = '', '' # message.get_args().split()
    
    for w in base.WEEKDAY_LIST:
        if w.lower() in reply_to_message:
            weekday = w
            break
    else:
        if not classroom:
            return

    for c in cnf.BotConfig.class_list:
        if c.lower() in reply_to_message:
            classroom = c
            break
    else:
        if not classroom:
            return
    
    async with state.proxy() as data:
        data['classroom'] = classroom
        data['weekday'] = base.WEEKDAYS[base.WEEKDAY_LIST.index(weekday)]

        await message.answer(base.CHANGE_TABLE_TEXT.format(classroom=data['classroom'], weekday=data['weekday']))

    await base.ChangeTable.table.set()


@dp.message_handler(state='*', commands="cancel")
async def cancelMessage(message: types.Message):
    current_state = await state.current_state()
    if not current_state:
        return

    await state.finish()

    await message.reply("OK, cancel")


@dp.message_handler(state=base.ChangeTable.table, is_owner=True)
async def changeTableState(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["table"] = message.text

        timetable = data["table"].split('|')
        for r in timetable:
            if r == timetable[0]:
                timetable = []

            timetable.append(r.split('/'))
        try:
            timetable = base.BuildTable(timetable, data["weekday"], data["classroom"])
        except IndexError:
            await message.reply(_(base.TABLE_ERROR))
            return

        await message.answer(_(base.CHANGE_TABLE_APPLY_TEXT.format(timetable)), reply_markup=keyboard.applyMarkup())
    return


@dp.callback_query_handler()
async def callbackQuery(call: types.callback_query):
    await call.answer(show_alert=True)

    pg.createTables()
    data: str = call.data
    message: types.Message = call.message

    if data in cnf.BotConfig.class_list:
        pg.setUserClass(call.from_user, data)
        await message.edit_text(_(base.CHOICE_WEEKDAY_TEXT), reply_markup=keyboard.weekdayChoice())

    elif data in base.WEEKDAYS:
        schedule_table = pg.getTimetable(call.from_user, data)
        schedule_table = base.BuildTable(schedule_table, base.WEEKDAY_LIST[base.WEEKDAYS.index(data)], pg.getUser(call.from_user)["classroom"])

        await message.edit_text(schedule_table, reply_markup=keyboard.startMarkup())

    elif "schedule" in data:
        
        if "my" in data:
            if not pg.getUser(call.from_user)["classroom"]:
                await message.edit_text(_(base.CHANGE_CLASSROOM_TEXT), reply_markup=keyboard.changeClassroom())
                return
            else:
                await message.edit_text(_(base.CHOICE_WEEKDAY_TEXT), reply_markup=keyboard.weekdayChoice())
                return

        elif "friend" in data:
            pass

    elif "change" in data:
        if "language" in data:
            pass
        elif "classroom" in data:
            await message.edit_text(_(base.CHANGE_CLASSROOM_TEXT), reply_markup=keyboard.changeClassroom())
            return


@dp.callback_query_handler(state=base.ChangeTable.table, is_owner=True)
async def changeTableCallback(call: types.callback_query, state: FSMContext):
    await call.answer(show_alert=True)

    data = call.data

    if "apply" in data:
        async with state.proxy() as data:
            print(type(data))
            pg.setTimetable(data)

            await call.message.edit_text(_(base.APPLIED_TABLE_TEXT))
    
    await state.finish()

async def on_startup(dp):
    await bot.delete_webhook()

    await bot.set_webhook(cnf.WebhookConfig.WEBHOOK_URL)

if __name__ == "__main__":
    pg.createTables()
    executor.start_webhook(dispatcher=dp, webhook_path=cnf.WebhookConfig.WEBHOOK_PATH, skip_updates=True, on_startup=on_startup, host='0.0.0.0', port=os.getenv("PORT"))
