import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from llm.client import get_llm_response
from llm.prompts import get_system_prompt

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Start command from user {user_id}")
    
    await message.answer("Привет! Я ваш персональный консультант. Чем могу помочь?")

async def handle_message(message: Message):
    """Обработчик текстовых сообщений через LLM"""
    try:
        user_id = message.from_user.id if message.from_user else "unknown"
        user_message = message.text
        
        logger.info(f"Message from user {user_id}: {user_message}")
        
        # Формируем запрос к LLM
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": user_message}
        ]
        
        # Получаем ответ от LLM
        response = await get_llm_response(messages)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Response sent to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await message.answer("Извините, произошла ошибка. Попробуйте еще раз.")

def setup_handlers(dp: Dispatcher):
    """Настройка обработчиков сообщений"""
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(handle_message) 