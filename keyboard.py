from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User
import base
from config import BotConfig


def startMarkup():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(callback_data='my-schedule', text=base.SCHEDULE_BUTTON_TEXT))
        # InlineKeyboardButton(callback_data='friend-schedule', text=base.FRIEND_SHEDULE_BUTTON_TEXT),
    
    markup.add(InlineKeyboardButton(callback_data='change-classroom', text=base.CHANGE_CLASSROOM_BUTTON_TEXT),
        # InlineKeyboardMarkup(callback_data='change-language', text=base.CHANGE_LANGUAGE_BUTTON_TEXT),
    )

    markup.add(InlineKeyboardButton(url=base.FEEDBACK_BUTTON_URL, text=base.FEEDBACK_BUTTON_TEXT))

    return markup

def changeClassroom():
    markup = InlineKeyboardMarkup(row_width=3)

    for i in BotConfig.class_list:
        markup.insert(InlineKeyboardButton(callback_data=i, text=i))
    
    return markup

def changeLanguage():
    markup = InlineKeyboardMarkup(row_width=3)

    for l in BotConfig.locales:
        markup.insert(InlineKeyboardButton(callback_data=l, text=l))
    
    return markup

def weekdayChoice():
    markup = InlineKeyboardMarkup(row_width=3)

    for o, w in zip(base.WEEKDAYS, base.WEEKDAY_LIST):
        markup.insert(InlineKeyboardButton(callback_data=o, text=w))
    
    return markup

def applyMarkup():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(callback_data='apply-table', text=base.APPLY_BUTTON_TEXT),
        InlineKeyboardButton(callback_data='edit-table', text=base.EDIT_BUTTON_TEXT)
    )

    return markup