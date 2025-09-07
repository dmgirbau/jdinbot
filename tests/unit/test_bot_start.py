import pytest
from aiogram.types import Message
from aiogram_tests.mocked_bot import MockedBot
from aiogram_tests.types.dataset import MESSAGE
from jdinbot.bot.handlers.commands.start import router

@pytest.mark.asyncio
async def test_start_command():
    """Test the /start command handler."""
    bot = MockedBot()
    message = Message(**MESSAGE, text="/start")
    
    call = await router.feed_message(bot, message)
    
    assert call is not None
    assert call.text == (
        "Welcome to JDINBot! 🎉\n"
        "Try /balance to check your balance or /help for more commands."
    )