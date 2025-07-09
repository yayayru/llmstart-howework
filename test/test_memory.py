import pytest
from llm.memory import (
    add_message_to_dialog, 
    get_dialog_history, 
    clear_dialog_history,
    get_dialog_stats,
    _dialogs
)

def test_add_message_to_dialog():
    """Тест добавления сообщения в диалог"""
    chat_id = 12345
    
    # Очищаем состояние перед тестом
    clear_dialog_history(chat_id)
    
    # Добавляем сообщение
    add_message_to_dialog(chat_id, "user", "Привет!")
    
    # Проверяем, что сообщение добавилось
    assert chat_id in _dialogs
    assert len(_dialogs[chat_id]) == 1
    assert _dialogs[chat_id][0]["role"] == "user"
    assert _dialogs[chat_id][0]["content"] == "Привет!"
    assert "timestamp" in _dialogs[chat_id][0]

def test_get_dialog_history():
    """Тест получения истории диалога"""
    chat_id = 12346
    
    # Очищаем состояние перед тестом
    clear_dialog_history(chat_id)
    
    # Добавляем несколько сообщений
    add_message_to_dialog(chat_id, "user", "Привет!")
    add_message_to_dialog(chat_id, "assistant", "Здравствуйте!")
    add_message_to_dialog(chat_id, "user", "Как дела?")
    
    # Получаем историю
    history = get_dialog_history(chat_id)
    
    # Проверяем корректность
    assert len(history) == 3
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Привет!"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Здравствуйте!"
    assert history[2]["role"] == "user"
    assert history[2]["content"] == "Как дела?"
    
    # Проверяем, что timestamp не включается в историю для LLM
    for msg in history:
        assert "timestamp" not in msg

def test_get_dialog_history_with_limit():
    """Тест ограничения количества сообщений в истории"""
    chat_id = 12347
    
    # Очищаем состояние перед тестом
    clear_dialog_history(chat_id)
    
    # Добавляем много сообщений
    for i in range(15):
        add_message_to_dialog(chat_id, "user", f"Сообщение {i}")
    
    # Получаем историю с лимитом
    history = get_dialog_history(chat_id, max_messages=5)
    
    # Проверяем, что возвращаются только последние 5 сообщений
    assert len(history) == 5
    assert history[0]["content"] == "Сообщение 10"
    assert history[4]["content"] == "Сообщение 14"

def test_get_dialog_history_empty():
    """Тест получения истории для несуществующего диалога"""
    chat_id = 99999
    
    # Получаем историю для несуществующего чата
    history = get_dialog_history(chat_id)
    
    # Проверяем, что возвращается пустой список
    assert history == []

def test_clear_dialog_history():
    """Тест очистки истории диалога"""
    chat_id = 12348
    
    # Добавляем сообщения
    add_message_to_dialog(chat_id, "user", "Привет!")
    add_message_to_dialog(chat_id, "assistant", "Здравствуйте!")
    
    # Проверяем, что сообщения есть
    assert len(get_dialog_history(chat_id)) == 2
    
    # Очищаем историю
    clear_dialog_history(chat_id)
    
    # Проверяем, что история очищена
    assert get_dialog_history(chat_id) == []
    assert chat_id not in _dialogs

def test_get_dialog_stats():
    """Тест получения статистики диалогов"""
    # Очищаем все диалоги
    _dialogs.clear()
    
    # Добавляем сообщения в разные чаты
    add_message_to_dialog(1, "user", "Привет!")
    add_message_to_dialog(1, "assistant", "Здравствуйте!")
    add_message_to_dialog(2, "user", "Как дела?")
    
    # Получаем статистику
    stats = get_dialog_stats()
    
    # Проверяем статистику
    assert stats["total_dialogs"] == 2
    assert stats["total_messages"] == 3 