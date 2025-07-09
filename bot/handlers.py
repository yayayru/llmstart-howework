import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Start command from user {user_id}")
    
    await message.answer("Привет! Я ваш персональный консультант. Чем могу помочь?")

def setup_handlers(dp: Dispatcher):
    """Настройка обработчиков сообщений"""
    dp.message.register(cmd_start, Command("start")) 