import gettext

user_lang = 'ru_RU'

lang_translations = gettext.translation('base', 'locale', languages=[user_lang])
lang_translations.install()

_ = lang_translations.gettext
