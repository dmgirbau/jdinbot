import sqlite3

from telegram import Update
from telegram.ext import CallbackContext

from src.db.dbconfiguration import connection
from src.db.solanaRequest import addreferbooonus,balance

REFERRAL_BONUS = 1.0  # Configurable referral bonus in JDIN


async def referral(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    async with connection() as conn:
        cursor = await conn.execute("SELECT unique_code FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()
        await cursor.close()

    if user:
        referral_code = user[0]
        await update.message.reply_text(f"Your referral code is: {referral_code}")
    else:
        await update.message.reply_text("You don't have an account. Use /start to create one.")


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

# Función para manejar el callback query 'insert_referral'
async def insert_referral_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
            chat_id=query.from_user.id,
            text="Por favor, ingresa el código de referido:"
        )
    context.user_data["awaiting_referral"] = True


# Función para manejar la entrada del código de referido
async def handle_referral_code_input(update: Update, context: CallbackContext):
    if not context.user_data.get("awaiting_referral"):
        return

    referral_code = update.message.text
    user = update.effective_user
    user_id = user.id
    username = user.username or "Anónimo"

    async with connection() as conn:
        cursor = await conn.execute("SELECT user_id FROM users WHERE unique_code = ?", (referral_code,))
        referrer = await cursor.fetchone()
        await cursor.close()

    if referrer:
        referrer_id = referrer[0]
        await addreferbooonus(referrer_id)
        await update.message.reply_text("Balance actualizado")
        bal = await balance(user_id)
        await context.bot.send_message(chat_id=user_id,text=f"Su balance actual es de {bal}")
    else:
        await update.message.reply_text("Código de referido inválido. Inténtalo de nuevo o omite este paso.")

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


# async def register_user(context: CallbackContext,user_id, username, input_referral_code, bonus, referrer_id=None):
#     new_referral_code = generate_referral_code(user_id)
#     try:
#         async with connection() as conn:
#             # Inicia una transacción (la forma exacta depende de la librería)
#             await conn.execute("BEGIN")
#
#             # Inserta el nuevo usuario
#             await conn.execute("""
#                 INSERT INTO users (user_id, username, referral_code, referrer, jdin_balance, has_used_referral)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             """, (user_id, username, new_referral_code, referrer_id, bonus, input_referral_code is not None))
#
#             # Si se proporcionó un referrer, actualiza su balance
#             if referrer_id:
#                 await conn.execute("""
#                     UPDATE users SET jdin_balance = jdin_balance + ?
#                     WHERE user_id = ?
#                 """, (bonus, referrer_id))
#
#                 # Opcional: notifica al referrer
#                 try:
#                     await context.bot.send_message(
#                         chat_id=referrer_id,
#                         text=f"¡Tu código de referido fue utilizado! Has ganado {bonus} JDIN como bono."
#                     )
#                 except Exception as e:
#                     print(f"Error al notificar al referrer: {e}")
#
#             # Confirma la transacción
#             await conn.commit()
#     except Exception as e:
#         # Si ocurre algún error, se podría hacer rollback y loggear el error
#         print(f"Error en register_user: {e}")
#         # Aquí podrías incluir await conn.rollback() si tu conexión lo soporta.


# def generate_referral_code(user_id: int) -> str:
#     return f"REF-{user_id}"