import os
from dotenv import load_dotenv

load_dotenv()

def get_telegram_token() -> str:
    """Получить токен Telegram бота из переменных окружения"""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN not found in environment variables")
    return token

def get_log_level() -> str:
    """Получить уровень логирования из переменных окружения"""
    return os.getenv("LOG_LEVEL", "INFO") 