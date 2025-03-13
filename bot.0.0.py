import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
import sqlite3
from uuid import uuid4
from random import randint

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('jdin_bot.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        jdin_balance REAL DEFAULT 0.0,
        pedjbono_id INTEGER,
        unique_code TEXT UNIQUE,
        solana_account TEXT,
        pending_request INTEGER DEFAULT 0
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
        tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user_id INTEGER,
        to_user_id INTEGER,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (from_user_id) REFERENCES users(user_id),
        FOREIGN KEY (to_user_id) REFERENCES users(user_id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS lojdin_statistics (
        lojdin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bet_amount REAL,
        outcome REAL,
        rolls INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    conn.commit()
    conn.close()

init_db()

# Bot Commands
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    conn = sqlite3.connect('jdin_bot.db')
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
    existing_user = cursor.fetchone()

    if existing_user:
        await update.message.reply_text(f"Welcome back, {user.first_name}! Your balance is {existing_user[2]:.4f} JDIN.")
    else:
        # Generate unique code
        unique_code = str(uuid4())[:8]
        cursor.execute("INSERT INTO users (user_id, username, unique_code) VALUES (?, ?, ?)", (user.id, user.username, unique_code))
        conn.commit()
        await update.message.reply_text(f"Welcome {user.first_name}! Your account has been created with code: {unique_code}")
    
    conn.close()

async def transfer(update: Update, context: CallbackContext):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /transfer <recipient_code> <amount>")
            return

        recipient_code = context.args[0]
        amount = float(context.args[1])

        if amount <= 0:
            await update.message.reply_text("Amount must be greater than 0.")
            return

        conn = sqlite3.connect('jdin_bot.db')
        cursor = conn.cursor()

        # Validate recipient
        cursor.execute("SELECT user_id FROM users WHERE unique_code = ?", (recipient_code,))
        recipient = cursor.fetchone()
        if not recipient:
            await update.message.reply_text("Recipient not found.")
            return

        recipient_id = recipient[0]

        # Check sender balance
        cursor.execute("SELECT jdin_balance FROM users WHERE user_id = ?", (update.effective_user.id,))
        sender = cursor.fetchone()
        if not sender or sender[0] < amount:
            await update.message.reply_text("Insufficient balance.")
            return

        # Update balances
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance - ? WHERE user_id = ?", (amount, update.effective_user.id))
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?", (amount, recipient_id))

        # Log transaction
        cursor.execute("INSERT INTO transactions (from_user_id, to_user_id, amount) VALUES (?, ?, ?)", (update.effective_user.id, recipient_id, amount))
        conn.commit()

        await update.message.reply_text(f"Successfully transferred {amount:.4f} JDIN to {recipient_code}.")
        conn.close()

    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a numeric value.")

async def balance(update: Update, context: CallbackContext):
    conn = sqlite3.connect('jdin_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT jdin_balance FROM users WHERE user_id = ?", (update.effective_user.id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        await update.message.reply_text(f"Your balance is {user[0]:.4f} JDIN.")
    else:
        await update.message.reply_text("You do not have an account. Use /start to create one.")

# Main Function
if __name__ == "__main__":
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("transfer", transfer))
    app.add_handler(CommandHandler("balance", balance))

    app.run_polling()

