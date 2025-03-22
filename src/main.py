import logging

from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler

from bot.comands import start, transfer, balance, gift_test
from gamble.comands import gamble, handle_gamble_amount, AWAITING_GAMBLE_AMOUNT
from config import AppConfig
from db.dbconfiguration import DataBase

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


gamble_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("tax", gamble)],
    states={
        AWAITING_GAMBLE_AMOUNT: [
            MessageHandler(Filters.text & ~Filters.command, handle_gamble_amount)
        ]
    },
    fallbacks=[]
)


def main():
    database = DataBase()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("transfer", transfer))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("gift", gift_test))
    app.add_handler(gamble_conversation_handler)

    # Start the bot
    logger.info("Polling...")
    app.run_polling()
    logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)