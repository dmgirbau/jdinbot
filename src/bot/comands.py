import sqlite3
from uuid import uuid4
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.db.dbconfiguration import connection

conn = sqlite3.connect("jdin_bot.db", check_same_thread=False)
cursor = conn.cursor()


async def start(update: Update, context: CallbackContext):
    user = update.effective_user

    # Verificar si el usuario ya existe en la base de datos
    async with connection() as conn:
        cursor = await conn.execute("SELECT jdin_balance, unique_code FROM users WHERE user_id = ?", (user.id,))
        existing_user = await cursor.fetchone()
        await cursor.close()

    if existing_user:
        balance, referral_code = existing_user
    else:
        # Generar un código de referido único para el nuevo usuario
        referral_code = str(uuid4())[:8]
        balance = 0.0  # Balance inicial

        async with connection() as conn:
            await conn.execute(
                "INSERT INTO users (user_id, username, balance, referral_code) VALUES (?, ?, ?, ?)",
                (user.id, user.username, balance, referral_code)
            )
            await conn.commit()

    # Crear el botón para insertar un código de referido
    keyboard = [
        [InlineKeyboardButton("Insertar código de referido", callback_data='insert_referral')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviar el mensaje con el balance, código de referido y el botón
    await update.message.reply_text(
        f"Bienvenido, {user.first_name}.\nTu balance actual es: {balance:.4f} JDIN.\nTu código de referido es: {referral_code}",
        reply_markup=reply_markup
    )


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
        cursor.execute("SELECT user_id FROM users WHERE unique_code = ?",
                       (recipient_code,))
        recipient = cursor.fetchone()
        if not recipient:
            await update.message.reply_text("Recipient not found.")
            return

        recipient_id = recipient[0]

        # Check sender balance
        cursor.execute("SELECT jdin_balance FROM users WHERE user_id = ?",
                       (update.effective_user.id,))
        sender = cursor.fetchone()
        if not sender or sender[0] < amount:
            await update.message.reply_text("Insufficient balance.")
            return

        # Update balances
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance - ? WHERE user_id = ?",
                       (amount, update.effective_user.id))
        cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?",
                       (amount, recipient_id))

        # Log transaction
        cursor.execute("INSERT INTO transactions (from_user_id, to_user_id, amount) VALUES (?, ?, ?)",
                       (update.effective_user.id, recipient_id, amount))
        conn.commit()

        await update.message.reply_text(f"Successfully transferred {amount:.4f} JDIN to {recipient_code}.")
        conn.close()

    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a numeric value.")


async def balance(update: Update, context: CallbackContext):
    conn = sqlite3.connect('jdin_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT jdin_balance FROM users WHERE user_id = ?",
                   (update.effective_user.id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        await update.message.reply_text(f"Your balance is {user[0]:.4f} JDIN.")
    else:
        await update.message.reply_text("You do not have an account. Use /start to create one.")


async def gift_test(update: Update, context: CallbackContext):
    conn = sqlite3.connect('jdin_bot.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET jdin_balance = jdin_balance + ? WHERE user_id = ?",
                   (100, update.effective_user.id))
    conn.commit()
    conn.close()