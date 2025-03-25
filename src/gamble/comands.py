import random
import sqlite3

from telegram import Update
from telegram.ext import CallbackContext

from src.db.solanaRequest import balance
from src.db.taxrequest import updatebalance, gambling_session, winingstatus, maxmultiplier


async def gamble(update: Update, context: CallbackContext):

    if not context.args:
        await update.message.reply_text("Please provide the amount you want to tax. Example: /tax 50")
        return
    try:
        bet_amount = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Please enter a valid amount.")
        return

    user_id = update.effective_user.id

    user = balance(user_id)

    if not user:
        await update.message.reply_text("You don't have an account. Use /start to create one.")
        return

    user_balance = user[0]
    if bet_amount <= 0 or bet_amount > user_balance:
        await update.message.reply_text("Invalid amount. Ensure it is greater than 0 and within your account balance.")
        return

    # Begin dice rolls
    streak = 0
    while True:
        roll = random.randint(1, 6)
        if roll == 6:
            streak += 1
            await update.message.reply_text(f"You rolled a 6! Streak: {streak}. Rolling again...")
        else:
            await update.message.reply_text(f"You rolled a {roll}. End of streak.")
            break

    # Calculate reward
    multiplier = 0
    winnings = 0
    if streak != 0:
        multiplier = 5 ** (streak - 1)
        winnings = bet_amount * multiplier
        await updatebalance(winnings,user_id)
        await update.message.reply_text(f"You got a winnings of {winnings}. That's a {multiplier + 1}X.")
    else:
        # Deduct bet amount from balance
        await updatebalance(bet_amount,user_id,mod="-")
        await update.message.reply_text(f"You already pay {bet_amount} in taxes, voluntary: You're a winner.")

    # Log the gambling session
        await gambling_session(user_id,bet_amount,multiplier,winnings,streak)

async def gambling_stats(update: Update, context: CallbackContext):
    """Provide statistics for gambling results."""
    total_games, total_winnings = winingstatus().fetchone()

    max_multiplier = maxmultiplier() or 0

    await update.message.reply_text(
        f"Gambling Statistics:\n"
        f"- Total Games Played: {total_games}\n"
        f"- Total Winnings Distributed: {total_winnings:.4f} JDIN\n"
        f"- Highest Multiplier Achieved: {max_multiplier:.2f}x"
    )
