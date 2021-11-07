import os

class BotConfig:
    APP_NAME = 'fivelyceum-schedulebot'
    OWNER_ID = 200635302
    DEFAULT_LANG = 'en_US'
    locales = os.listdir("locale")
    
    class_list= list(str(i) + '-' + n for i in range(6, 12) for n in ["А", "Б", "В"])

class DevelopmentConfig:
    API_TOKEN = os.getenv("API_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")

class ProductionConfig:
    API_TOKEN = os.getenv("API_TOKEN") # Your API Token here
    DATABASE_URL = os.getenv("DATABASE_URL") # Database url here (postgres://user:password@host:port/database)


class WebhookConfig:
    REPO_NAME = BotConfig.APP_NAME
    WEBHOOK_PATH = f"/webhook/{DevelopmentConfig.API_TOKEN}"
    WEBHOOK_URL = f'https://{REPO_NAME}.herokuapp.com' + WEBHOOK_PATH