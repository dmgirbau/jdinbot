import logging

from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from src.bot.comands import start, transfer, balance, gift_test
from src.gamble.comands import gamble
from src.config import AppConfig
from src.db.dbconfiguration import DataBase

config = AppConfig()
TELEGRAM_TOKEN = config.TELEGRAM_TOKEN
APP_MODE = config.APP_MODE

# Logger configuration
if APP_MODE == "dev":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
else:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
    )

logger = logging.getLogger(__name__)


def main():
    database = DataBase()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("transfer", transfer))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("gift", gift_test))
    app.add_handler(CommandHandler("tax", gamble))

    # Start the bot
    logger.info("Polling...")
    app.run_polling()
    logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)