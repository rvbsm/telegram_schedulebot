from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import User
from database.postgresql import PostgreSQLDatabase
import config as cnf
import base
import sys, os

env = sys.argv[1]

if env == "dev":
    config = cnf.DevelopmentConfig
else:
    config = cnf.ProductionConfig

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot=bot)
pg = PostgreSQLDatabase(os.getenv("DATABASE_URL"))


@dp.message_handler(commands=["start"])
async def startMessage(message: types.Message):
    base.LangSwitch(message)

    if not pg.getUser(message.from_user):
        pg.addUser(message.from_user)

        await message.answer(base.HELLO_MESSAGE_TEXT)
    await message.answer(base.START_MESSAGE_TEXT)

@dp.message_handler(commands=["help"])
async def helpMessage(message: types.Message):
    return

@dp.message_handler(commands=["lang"])
async def langMessage(message: types.Message):
    if message.get_args() and message.get_args() in cnf.BotConfig.locales:
        pg.setUserLocale(message.from_user, message.get_args()[0])
        return
    
    await message.answer(base.CHANGE_LANG_TEXT)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)




# # # # # # # # # # # # # # # # # # # # # # # # # #

user = {
    'id': 200635301,
    'is_bot': False,
    'first_name': "Руслан",
    'last_name': "",
    'username': "rvbsm",
    'language_code': "en_US",
    'can_join_groups': True,
    'can_read_all_group_messages': True,
    'supports_inline_queries': True
}
user = User(**user)
print(pg.getUser(user))
"""
timetable_example = "\nSubject: {}\nTeacher: {}\nTime: {}"
weekday = "monday"
timetable = pg.getTimetable(user, weekday)
time = pg.getTime(weekday in cnf.BotConfig.abb_days)

for n, t in zip(range(len(timetable)), time):
    timetable[n].append(t)

timetable_text = []
for lesson in timetable:

    timetable_text.append(str(timetable.index(lesson)+1) + timetable_example.format(*lesson))

print('\n\n'.join(timetable_text))
"""