import os

class BotConfig:
    APP_NAME = 'schedulebot'
    OWNER_ID = 0
    DEFAULT_LANG = 'en_US'
    locales = os.listdir("locale")
    
    abb_days = ["monday", "saturday"]

class DevelopmentConfig:
    API_TOKEN = os.getenv("API_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")

class ProductionConfig:
    API_TOKEN = os.getenv("API_TOKEN") # Your API Token here
    DATABASE_URL = os.getenv("DATABASE_URL") # Database url here (postgres://user:password@host:port/database)


class WebhookConfig:
    REPO_NAME = BotConfig.APP_NAME
    WEBHOOK_URL = f'https://{REPO_NAME}.herokuapp.com/webhook/{DevelopmentConfig.API_TOKEN}'