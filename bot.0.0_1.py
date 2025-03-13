import sqlite3
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import random
from datetime import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect('jdin_bot.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE,
                    code TEXT UNIQUE,
                    balance REAL DEFAULT 0.0,
                    pedjbono_code TEXT,
                    solana_account TEXT,
                    approved INTEGER DEFAULT 0,
                    registered_by INTEGER
                )''')
    
    # Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER,
                    recipient_id INTEGER,
                    amount REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    
    # JDIN Offerings stats
    c.execute('''CREATE TABLE IF NOT EXISTS offerings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    result INTEGER,
                    amount REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    
    conn.commit()
    conn.close()

# Generate unique user codes
def generate_codes():
    codes = [f"JDIN-{random.randint(100000, 999999)}" for _ in range(100000)]
    return list(set(codes))[:99490300]

available_codes = generate_codes()

# Get unique code
def get_unique_code():
    if not available_codes:
        raise ValueError("No more codes available!")
    return available_codes.pop()

# Start command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    conn = sqlite3.connect('jdin_bot.db')
    c = conn.cursor()

    # Check if user exists
    c.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    user = c.fetchone()
    
    if user:
        update.message.reply_text(f"You already have an account! Your code: {user[2]}\nBalance: {user[3]:.4f} JDIN")
    else:
        # Create new account
        unique_code = get_unique_code()
        c.execute("INSERT INTO users (telegram_id, code, balance) VALUES (?, ?, 1.0)", (user_id, unique_code))
        conn.commit()
        update.message.reply_text(f"Welcome! Your account has been created.\nYour code: {unique_code}\nInitial Balance: 1.0 JDIN")
    
    conn.close()

# Transfer command
def transfer(update: Update, context: CallbackContext):
    try:
        sender_id = update.effective_user.id
        args = context.args

        if len(args) != 2:
            update.message.reply_text("Usage: /transfer <recipient_code> <amount>")
            return
    
        recipient_code, amount = args[0], float(args[1])
    
        conn = sqlite3.connect('jdin_bot.db')
        c = conn.cursor()
    
        # Validate sender
        c.execute("SELECT user_id, balance FROM users WHERE telegram_id = ?", (sender_id,))
        sender = c.fetchone()
    
        if not sender:
            update.message.reply_text("You don't have an account! Use /start to create one.")
            conn.close()
            return
    
        sender_user_id, sender_balance = sender
    
        if sender_balance < amount:
            update.message.reply_text("Insufficient balance.")
            conn.close()
            return
    
        # Validate recipient
        c.execute("SELECT user_id FROM users WHERE code = ?", (recipient_code,))
        recipient = c.fetchone()
    
        if not recipient:
            update.message.reply_text("Recipient not found.")
            conn.close()
            return
    
        recipient_user_id = recipient[0]
    
        # Process transfer
        c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, sender_user_id))
        c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, recipient_user_id))
    
        # Log transaction
        c.execute("INSERT INTO transactions (sender_id, recipient_id, amount) VALUES (?, ?, ?)",
                  (sender_user_id, recipient_user_id, amount))
    
        conn.commit()
        conn.close()
    
        update.message.reply_text(f"Transfer successful! You sent {amount:.4f} JDIN to {recipient_code}.")
    
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Main function
def main():
    setup_database()
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("transfer", transfer))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()