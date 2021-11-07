from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import BoundFilter
from database.postgresql import PostgreSQLDatabase
from config import BotConfig, ProductionConfig
from aiogram.contrib.middlewares.i18n import I18nMiddleware

pg = PostgreSQLDatabase(ProductionConfig.DATABASE_URL)

class ChangeTable(StatesGroup):
    weekday = State()
    classroom = State()
    table = State()

class IsOwner(BoundFilter):
    key = "is_owner"

    def __init__(self, is_owner):
        self.is_owner = is_owner

    async def check(self, message: types.Message):
        return message.from_user.id == BotConfig.OWNER_ID


def BuildTable(table: list[list[str]], weekday: str, classroom: str):
    time = pg.getTime(weekday in ABB_DAYS)

    for n, t in zip(range(len(table)), time):
        table[n].append(t)

    timetable = []

    for index, lesson in enumerate(table, start=1):

        timetable.append(str(index) + TIMETABLE_TEMPLATE.format(*lesson))

    return TIMETABLE_HEADER.format(classroom=classroom, weekday=weekday) + '\n\n'.join(timetable)


ABB_DAYS = ["Monday", "Saturday"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
WEEKDAY_LIST = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

TIMETABLE_HEADER = "Расписание для {classroom} на {weekday}:\n"
TIMETABLE_TEMPLATE = "\nПредмет: {}\nУчитель: {}\nВремя: {}"

START_MESSAGE_TEXT = "Рад тебя видеть снова"
CHANGE_LANG_TEXT = "Доступные языки:"
CHANGE_TABLE_TEXT = "Write the new table for {classroom} on {weekday}\n \"Subject/Teacher|Subject/Teacher\" or \"Subject, Subject/Teacher, Teacher\""
CHANGE_TABLE_APPLY_TEXT = "Timetable looks like this: {}"
APPLIED_TABLE_TEXT = "Updated timetable"
TABLE_ERROR = "ERROR"
HELP_MESSAGE_TEXT = "This is an help message"
CHANGE_CLASSROOM_TEXT = "Из какого ты класса?"
CHOICE_WEEKDAY_TEXT = "Какой день недели?"


SCHEDULE_BUTTON_TEXT = "Моё расписание"
FRIEND_SHEDULE_BUTTON_TEXT = "Расписание друга"
CHANGE_CLASSROOM_BUTTON_TEXT = "Сменить класс"
CHANGE_LANGUAGE_BUTTON_TEXT = "Сменить язык"
FEEDBACK_BUTTON_URL = "t.me/rvbsm"
FEEDBACK_BUTTON_TEXT = "Разработчик"

APPLY_BUTTON_TEXT = "Apply"
EDIT_BUTTON_TEXT = "Cancel"
