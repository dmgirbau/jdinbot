import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Constants
REFERRAL_BONUS = 1.0  # Configurable referral bonus in JDIN

# Database setup
conn = sqlite3.connect("jdin_bot.db", check_same_thread=False)
cursor = conn.cursor()

# Ensure tables exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    referral_code TEXT UNIQUE,
    referrer TEXT,
    jdin_balance REAL DEFAULT 0.0,
    has_used_referral BOOLEAN DEFAULT FALSE
)
""")
conn.commit()

# Generate referral codes
def generate_referral_code(user_id: int) -> str:
    return f"REF-{user_id}"

# /start command
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    username = user.username or "Anonymous"

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        update.message.reply_text("You already have an account!")
        return

    # Handle referral code
    referrer_id = None
    if context.args:
        referral_code = context.args[0]
        cursor.execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,))
        referrer = cursor.fetchone()
        if referrer:
            referrer_id = referrer[0]
            cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?",
                           (REFERRAL_BONUS, referrer_id))
        else:
            update.message.reply_text("Invalid referral code. Proceeding without a referral.")

    # Create account
    referral_code = generate_referral_code(user_id)
    cursor.execute("""
        INSERT INTO users (user_id, username, referral_code, referrer, jdin_balance, has_used_referral)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, referral_code, referrer_id, REFERRAL_BONUS if referrer_id else 0.0, referrer_id is not None))
    conn.commit()

    # Notify user
    update.message.reply_text(
        f"Welcome, {username}! Your account has been created.\n"
        f"Your referral code is: {referral_code}\n"
        f"Starting balance: {REFERRAL_BONUS if referrer_id else 0.0} JDIN."
    )

# Main function to set up bot
def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

