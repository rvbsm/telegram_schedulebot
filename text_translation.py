import gettext
import string

from psycopg2 import connect

user_lang = 'ru_RU'

lang_translations = gettext.translation('base', 'locale', languages=[user_lang])
lang_translations.install()

_ = lang_translations.gettext

text = "Schedule for \"11-Б\""
for c in ["11-А", "11-Б", "11-В"]:
    try:
        result = text[text.index(c)]
    except ValueError:
        continue
    
    if result:
        print(result)