import os
import pytest
from config import get_log_level, get_telegram_token

def test_get_log_level_default():
    """Тест получения уровня логирования по умолчанию"""
    # Удаляем переменную если она есть
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]
    
    level = get_log_level()
    assert level == "INFO"

def test_get_log_level_custom():
    """Тест получения кастомного уровня логирования"""
    os.environ["LOG_LEVEL"] = "DEBUG"
    level = get_log_level()
    assert level == "DEBUG"
    
    # Очищаем после теста
    del os.environ["LOG_LEVEL"]

def test_get_telegram_token_exists():
    """Тест получения токена из переменных окружения"""
    # Проверяем что токен загружается из .env файла
    token = get_telegram_token()
    assert token is not None
    assert len(token) > 10  # Минимальная проверка формата токена

def test_get_telegram_token_from_env():
    """Тест получения токена из переменной окружения"""
    test_token = "test_token_123"
    original_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    # Устанавливаем тестовый токен
    os.environ["TELEGRAM_BOT_TOKEN"] = test_token
    
    try:
        # Перезагружаем модуль или вызываем функцию снова
        from importlib import reload
        import config
        reload(config)
        
        assert config.get_telegram_token() == test_token
    finally:
        # Восстанавливаем оригинальное значение
        if original_token:
            os.environ["TELEGRAM_BOT_TOKEN"] = original_token
        elif "TELEGRAM_BOT_TOKEN" in os.environ:
            del os.environ["TELEGRAM_BOT_TOKEN"] 