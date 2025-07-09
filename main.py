import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import get_telegram_token, get_log_level
from bot.handlers import setup_handlers

async def main():
    """Основная функция запуска бота"""
    logger = logging.getLogger(__name__)
    logger.info("Starting Telegram bot")
    
    # Создание бота и диспетчера
    bot = Bot(token=get_telegram_token())
    dp = Dispatcher()
    
    # Настройка обработчиков
    setup_handlers(dp)
    
    # Запуск бота
    try:
        logger.info("Bot is running. Press Ctrl+C to stop.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        await bot.session.close()
        logger.info("Bot session closed")

if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, get_log_level()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise 