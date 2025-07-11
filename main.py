import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import get_telegram_token, get_log_level
from bot.handlers import setup_handlers
from llm.logging_utils import setup_detailed_logging

async def main():
    """Основная функция приложения"""
    logger = logging.getLogger(__name__)
    
    # Инициализация бота
    bot = Bot(token=get_telegram_token())
    dp = Dispatcher()
    
    # Регистрация обработчиков
    setup_handlers(dp)
    
    logger.info("Starting bot...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error during bot polling: {str(e)}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Настройка логирования только через детальную функцию
    setup_detailed_logging()
    logger = logging.getLogger(__name__)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise 