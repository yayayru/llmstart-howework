import os
import pytest
from config import get_telegram_token, get_log_level

def test_get_log_level_default():
    """Тест получения уровня логирования по умолчанию"""
    # Удаляем переменную окружения если она есть
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]
    
    assert get_log_level() == "INFO"

def test_get_log_level_custom():
    """Тест получения пользовательского уровня логирования"""
    os.environ["LOG_LEVEL"] = "DEBUG"
    assert get_log_level() == "DEBUG"
    
    # Очищаем после теста
    del os.environ["LOG_LEVEL"]

def test_get_telegram_token_missing():
    """Тест ошибки при отсутствии токена"""
    # Удаляем переменную окружения если она есть
    if "TELEGRAM_TOKEN" in os.environ:
        del os.environ["TELEGRAM_TOKEN"]
    
    with pytest.raises(ValueError, match="TELEGRAM_TOKEN not found"):
        get_telegram_token()

def test_get_telegram_token_exists():
    """Тест получения токена из переменных окружения"""
    test_token = "test_token_123"
    os.environ["TELEGRAM_TOKEN"] = test_token
    
    assert get_telegram_token() == test_token
    
    # Очищаем после теста
    del os.environ["TELEGRAM_TOKEN"] 