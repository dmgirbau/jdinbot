import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
    has_used_referral BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    # Ask for referral code via buttons
    keyboard = [
        [InlineKeyboardButton("Enter Referral Code", callback_data="enter_referral")],
        [InlineKeyboardButton("Skip", callback_data="skip_referral")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Do you have a referral code?", reply_markup=reply_markup)

# Callback for referral choice
def handle_referral_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    user_id = user.id
    username = user.username or "Anonymous"

    if query.data == "enter_referral":
        query.edit_message_text("Please send your referral code as a message.")
        context.user_data["awaiting_referral"] = True
    elif query.data == "skip_referral":
        register_user(user_id, username, None, 0.0)
        query.edit_message_text("Account created without a referral code.")

# Referral code input
def handle_referral_code_input(update: Update, context: CallbackContext):
    if not context.user_data.get("awaiting_referral"):
        return

    referral_code = update.message.text
    user = update.effective_user
    user_id = user.id
    username = user.username or "Anonymous"

    # Validate referral code
    cursor.execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,))
    referrer = cursor.fetchone()
    if referrer:
        referrer_id = referrer[0]
        register_user(user_id, username, referral_code, REFERRAL_BONUS, referrer_id)
        update.message.reply_text(f"Account created! Referral bonus applied.")
    else:
        update.message.reply_text("Invalid referral code. Try again or skip.")
    context.user_data["awaiting_referral"] = False

# Register a new user

###   Referral Bonus to the referrer implementation

#def register_user(user_id, username, referral_code, bonus, referrer_id=None):
#    """
#    Registers a new user. If a referrer ID is provided, credit the referrer with the referral bonus.
#    """
#    new_referral_code = generate_referral_code(user_id)

    # Create new user account
#    cursor.execute("""
#        INSERT INTO users (user_id, username, referral_code, referrer, jdin_balance, has_used_referral)
#        VALUES (?, ?, ?, ?, ?, ?)
#    """, (user_id, username, new_referral_code, referrer_id, bonus, referral_code is not None))
#
#    # Credit the referrer, if applicable
#    if referrer_id:
#        cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?", 
#                       (REFERRAL_BONUS, referrer_id))
#
#        # Optional: Notify the referrer about the bonus
#        # This assumes the bot object is available globally
#        try:
#            bot.send_message(chat_id=referrer_id, 
#                             text=f"Your referral code was used! You've earned {REFERRAL_BONUS} JDIN as a bonus.")
#        except Exception as e:
#           print(f"Could not notify referrer: {e}")
#
#    conn.commit()
#

def register_user(user_id, username, referral_code, bonus, referrer_id=None):
    new_referral_code = generate_referral_code(user_id)
    cursor.execute("""
        INSERT INTO users (user_id, username, referral_code, referrer, jdin_balance, has_used_referral)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, new_referral_code, referrer_id, bonus, referral_code is not None))
    if referrer_id:
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?", (bonus, referrer_id))
    conn.commit()

# /referral command
def referral(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    cursor.execute("SELECT referral_code FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        referral_code = user[0]
        update.message.reply_text(f"Your referral code is: {referral_code}")
    else:
        update.message.reply_text("You don't have an account. Use /start to create one.")

# Main function to set up bot
def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("referral", referral))
    dp.add_handler(CommandHandler("handle_referral_code_input", handle_referral_code_input))
    dp.add_handler(CallbackQueryHandler(handle_referral_choice))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

