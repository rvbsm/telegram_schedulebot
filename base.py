from database.postgresql import PostgreSQLDatabase
from config import ProductionConfig
import gettext

pg = PostgreSQLDatabase(ProductionConfig.DATABASE_URL)

lang_translations = gettext.translation('base', 'locale', languages=['ru_RU'])

def LangSwitch(self, message):
    lang_translations = gettext.translation('base', 'locale', languages=[pg.getUser(message.from_user)["locale"]])
    lang_translations.install()

_ = lang_translations.gettext

HELLO_MESSAGE_TEXT = _("Hello")
START_MESSAGE_TEXT = _("Nice to see you again")
CHANGE_LANG_TEXT = _("ru_RU or en_US?")
