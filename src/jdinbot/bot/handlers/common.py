from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
await message.answer(
"👋 Welcome to <b>JDINBot</b>!\n\nUse /help to see available commands."
)


@router.message(Command("help"))
async def cmd_help(message: Message):
await message.answer(
"Available commands:\n"
"• /start — welcome\n"
"• /help — this help"
)