import sqlite3

from telegram import Update
from telegram.ext import CallbackContext

from src.db.dbconfiguration import connection

REFERRAL_BONUS = 1.0  # Configurable referral bonus in JDIN


async def referral(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = await connection().execute("SELECT referral_code FROM users WHERE user_id = ?", (user_id,)).fetchone()

    if user:
        referral_code = user[0]
        await update.message.reply_text(f"Your referral code is: {referral_code}")
    else:
        await update.message.reply_text("You don't have an account. Use /start to create one.")


async def handle_referral_code_input(update: Update, context: CallbackContext):
    if not context.user_data.get("awaiting_referral"):
        return

    referral_code = update.message.text
    user = update.effective_user
    user_id = user.id
    username = user.username or "Anonymous"

    # Validate referral code
    referrer = await connection().execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,)).fetchone()
    if referrer:
        referrer_id = referrer[0]
        await register_user(user_id, username, referral_code, REFERRAL_BONUS, referrer_id)
        await update.message.reply_text(f"Account created! Referral bonus applied.")
    else:
        await update.message.reply_text("Invalid referral code. Try again or skip.")
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


async def register_user(user_id, username, referral_code, bonus, referrer_id=None):
    new_referral_code = generate_referral_code(user_id)
    await connection().execute("""
        INSERT INTO users (user_id, username, referral_code, referrer, jdin_balance, has_used_referral)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, new_referral_code, referrer_id, bonus, referral_code is not None))
    if referrer_id:
        await connection().execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?", (bonus, referrer_id)).commit()
def generate_referral_code(user_id: int) -> str:
    return f"REF-{user_id}"