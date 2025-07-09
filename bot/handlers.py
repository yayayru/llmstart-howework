import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from llm.client import get_llm_response
from llm.prompts import get_system_prompt
from llm.memory import add_message_to_dialog, get_dialog_history, clear_dialog_history

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    """Обработчик команды /start"""
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Start command from user {user_id} in chat {chat_id}")
    
    # Очищаем историю диалога при старте
    clear_dialog_history(chat_id)
    
    welcome_message = "Привет! Я ваш персональный консультант для первичной консультации. Расскажите, какие у вас есть вопросы или потребности, и я помогу подобрать подходящие услуги нашей компании."
    
    # Сохраняем приветственное сообщение в историю
    add_message_to_dialog(chat_id, "assistant", welcome_message)
    
    await message.answer(welcome_message)

async def handle_message(message: Message):
    """Обработчик текстовых сообщений через LLM с сохранением контекста"""
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else "unknown"
        user_message = message.text
        
        logger.info(f"Message from user {user_id} in chat {chat_id}: {user_message}")
        
        # Добавляем сообщение пользователя в историю
        add_message_to_dialog(chat_id, "user", user_message)
        
        # Получаем историю диалога (последние 10 сообщений)
        history = get_dialog_history(chat_id, max_messages=10)
        
        # Формируем запрос к LLM с системным промптом и историей
        messages = [{"role": "system", "content": get_system_prompt()}] + history
        
        logger.info(f"Sending {len(messages)} messages to LLM (including system prompt)")
        
        # Получаем ответ от LLM
        response = await get_llm_response(messages)
        
        # Сохраняем ответ в историю
        add_message_to_dialog(chat_id, "assistant", response)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Response sent to user {user_id} in chat {chat_id}")
        
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await message.answer("Извините, произошла ошибка. Попробуйте еще раз.")

def setup_handlers(dp: Dispatcher):
    """Настройка обработчиков сообщений"""
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(handle_message) 