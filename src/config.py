import os
from dotenv import load_dotenv

class AppConfig:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
        load_dotenv(dotenv_path)
        self.TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
        self.APP_MODE = os.getenv("APP_MODE", "dev").lower()
