from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="start")

@router.message(Command(commands=["start"]))
async def handle_start(message: Message) -> None:
    """Handle the /start command by sending a welcome message."""
    await message.answer(
        "Welcome to JDINBot! 🎉\n"
        "Try /balance to check your balance or /help for more commands."
    )