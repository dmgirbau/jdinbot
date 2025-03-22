import random
import sqlite3

from telegram import Update
from telegram.ext import CallbackContext

conn = sqlite3.connect("jdin_bot.db", check_same_thread=False)
cursor = conn.cursor()


def gamble(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    cursor.execute("SELECT jdin_balance FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        update.message.reply_text("You don't have an account. Use /start to create one.")
        return

    user_balance = user[0]
    update.message.reply_text(f"Your current balance is {user_balance:.4f} JDIN. Enter the amount you'd like to gamble:")

    context.user_data["awaiting_gamble_amount"] = True


def handle_gamble_amount(update: Update, context: CallbackContext):
    if not context.user_data.get("awaiting_gamble_amount"):
        return

    try:
        bet_amount = float(update.message.text)
    except ValueError:
        update.message.reply_text("Please enter a valid amount.")
        return

    cursor.execute("SELECT jdin_balance FROM users WHERE user_id = ?", (update.effective_user.id,))
    user_balance = cursor.fetchone()[0]

    if bet_amount <= 0 or bet_amount > user_balance:
        update.message.reply_text("Invalid amount. Ensure it is greater than 0 and within your account balance.")
        return

    # Begin dice rolls
    rolls = []
    streak = 0
    while True:
        roll = random.randint(1, 6)
        rolls.append(roll)
        if roll == 6:
            streak += 1
            update.message.reply_text(f"You rolled a 6! Streak: {streak}. Rolling again...")
        else:
            update.message.reply_text(f"You rolled a {roll}. End of streak.")
            break

    # Calculate reward
    multiplier = 0
    winnings = 0
    if streak != 0:
        multiplier = 5 ** (streak - 1)
        winnings = bet_amount * multiplier
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?", (winnings, update.effective_user.id))
        conn.commit()
        update.message.reply_text(f"You got a winnings of {winnings}. That's a {multiplier + 1}X.")
    else:
        # Deduct bet amount from balance
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance - ? WHERE user_id = ?",(bet_amount, update.effective_user.id))
        conn.commit()
        update.message.reply_text(f"You already pay {bet_amount} in taxes, voluntary: You're a winner.")

    # Log the gambling session
    cursor.execute("""INSERT INTO gambling_logs (user_id, bet_amount, multiplier, winnings, streak) VALUES (?, ?, ?, ?, ?)""", (update.effective_user.id, bet_amount, multiplier, winnings, streak))
    conn.commit()
    context.user_data["awaiting_gamble_amount"] = False


def gambling_stats(update: Update, context: CallbackContext):
    """Provide statistics for gambling results."""
    cursor.execute("SELECT COUNT(*), SUM(winnings) FROM gambling_logs")
    total_games, total_winnings = cursor.fetchone()

    cursor.execute("SELECT MAX(multiplier) FROM gambling_logs")
    max_multiplier = cursor.fetchone()[0] or 0

    update.message.reply_text(
        f"Gambling Statistics:\n"
        f"- Total Games Played: {total_games}\n"
        f"- Total Winnings Distributed: {total_winnings:.4f} JDIN\n"
        f"- Highest Multiplier Achieved: {max_multiplier:.2f}x"
    )
