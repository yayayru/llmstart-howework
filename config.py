import os
from dotenv import load_dotenv

load_dotenv()

def get_telegram_token() -> str:
    """Получить токен Telegram бота из переменных окружения"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    return token

def get_log_level() -> str:
    """Получить уровень логирования из переменных окружения"""
    return os.getenv("LOG_LEVEL", "INFO")

def get_openrouter_api_key() -> str:
    """Получить ключ API OpenRouter из переменных окружения"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    return api_key

def get_llm_model() -> str:
    """Получить модель LLM из переменных окружения"""
    return os.getenv("LLM_MODEL", "anthropic/claude-3-haiku")

def get_llm_timeout() -> int:
    """Получить таймаут для запросов к LLM"""
    return int(os.getenv("LLM_TIMEOUT", "30")) 