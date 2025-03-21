import sqlite3
from http.client import responses

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.config import AppConfig
from src.db.dbconfiguration import connection
from src.db.solanaRequest import verifysolanaacount, balance, descountfee, solanarequest, transactioStatus, \
    transactionUpdateSatus, insertransaction


def request_solana(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    acount = verifysolanaacount(user_id)
    if acount.fetchone():
        update.message.reply_text("You already have an approved Solana address.")
        return

    keyboard = [
        [InlineKeyboardButton("Use Existing Address", callback_data="solana_existing")],
        [InlineKeyboardButton("Request New Address Preparation", callback_data="solana_new")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose an option for your Solana account setup:", reply_markup=reply_markup)
def handle_solana_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "solana_existing":
        query.edit_message_text("Send your existing Solana address:")
        context.user_data["solana_request_type"] = "existing"
    elif query.data == "solana_new":
        query.edit_message_text("A new Solana account preparation will be requested. Proceeding...")
        process_solana_request(context,update,user_id, "new", None)
async def process_solana_request(context: CallbackContext,update: Update,user_id: int, request_type: str, address: str = None,):
    # Fetch the fee based on type
    fee = 2.0 if request_type == "new" else 1.0  # Example fees

    user_balance =  await balance(user_id)[0]

    if user_balance < fee:
        await update.message.reply_text("Insufficient JDIN balance for this request.")
        return

    # Deduct fee and record the request
    await descountfee(fee,user_id)
    await solanarequest(user_id,address,request_type,fee)
    await update.message.reply_text(f"Request submitted for {request_type} address setup. Fee: {fee} JDIN.")

    # Notify the admin
    ADMIN_CHAT = AppConfig().ADMIN_CHAT  # Replace with the actual admin chat ID
    await context.bot.send_message(chat_id=ADMIN_CHAT, text=f"New Solana setup request from user {user_id} (Type: {request_type}).")
# Handle Solana address input
async def handle_solana_address(update: Update, context: CallbackContext):
    if "solana_request_type" not in context.user_data:
        await update.message.reply_text("No Solana setup request in progress.")
        return

    address = update.message.text.strip()
    if not validate_solana_address(address):
        await update.message.reply_text("Invalid Solana address. Please try again.")
        return

    user_id = update.effective_user.id
    await process_solana_request(user_id, context.user_data["solana_request_type"], address)
    del context.user_data["solana_request_type"]
def validate_solana_address(address: str) -> bool:
    return len(address) == 44  # Simplistic validation
async def approve_solana(update: Update, context: CallbackContext):
    user_id = int(context.args[0]) if context.args else None

    if not user_id:
        await update.message.reply_text("Usage: /approve_solana <user_id>")
        return


    request = transactioStatus(user_id)

    if not request:
        await update.message.reply_text("No pending requests for this user.")
        return

    solana_address = request[2]
    request_type = request[3]

    # Approve the request
    await transactionUpdateSatus(user_id)
    await insertransaction(user_id,solana_address)

    await update.message.reply_text(f"Request approved for user {user_id}. Solana address: {solana_address}")
    await context.bot.send_message(chat_id=user_id, text=f"Your Solana address has been approved: {solana_address}")


