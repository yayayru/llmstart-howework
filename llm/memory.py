import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Глобальное хранилище диалогов в памяти
# Структура: {chat_id: [{"role": "user/assistant", "content": "...", "timestamp": datetime}]}
_dialogs: Dict[int, List[Dict[str, str]]] = {}

def get_dialog_history(chat_id: int, max_messages: int = 10) -> List[Dict[str, str]]:
    """
    Получить историю диалога для чата (последние N сообщений)
    
    Args:
        chat_id: ID чата
        max_messages: Максимальное количество сообщений для возврата
        
    Returns:
        Список сообщений в формате [{"role": "user/assistant", "content": "..."}]
    """
    if chat_id not in _dialogs:
        return []
    
    # Возвращаем последние max_messages сообщений без timestamp для LLM
    messages = _dialogs[chat_id][-max_messages:]
    return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

def add_message_to_dialog(chat_id: int, role: str, content: str) -> None:
    """
    Добавить сообщение в историю диалога
    
    Args:
        chat_id: ID чата
        role: Роль отправителя (user/assistant/system)
        content: Содержание сообщения
    """
    if chat_id not in _dialogs:
        _dialogs[chat_id] = []
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    _dialogs[chat_id].append(message)
    logger.info(f"Added message to dialog {chat_id}: role={role}, content_length={len(content)}")

def clear_dialog_history(chat_id: int) -> None:
    """
    Очистить историю диалога для чата
    
    Args:
        chat_id: ID чата
    """
    if chat_id in _dialogs:
        del _dialogs[chat_id]
        logger.info(f"Cleared dialog history for chat {chat_id}")

def get_dialog_stats() -> Dict[str, int]:
    """
    Получить статистику диалогов
    
    Returns:
        Словарь со статистикой диалогов
    """
    total_dialogs = len(_dialogs)
    total_messages = sum(len(messages) for messages in _dialogs.values())
    
    return {
        "total_dialogs": total_dialogs,
        "total_messages": total_messages
    } 