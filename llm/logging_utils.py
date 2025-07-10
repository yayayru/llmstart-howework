"""
Утилиты для расширенного логирования
"""
import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from llm.memory import get_dialog_stats

logger = logging.getLogger(__name__)

class MetricsLogger:
    """Класс для сбора и логирования метрик производительности"""
    
    def __init__(self):
        self.metrics = {}
    
    def log_llm_request(self, 
                       user_id: str, 
                       chat_id: int, 
                       messages_count: int, 
                       model: str,
                       start_time: float,
                       end_time: float,
                       success: bool,
                       error: Optional[str] = None,
                       response_length: Optional[int] = None):
        """Логировать метрики запроса к LLM"""
        
        elapsed_time = end_time - start_time
        
        metric_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "llm_request",
            "user_id": user_id,
            "chat_id": chat_id,
            "messages_count": messages_count,
            "model": model,
            "elapsed_time": round(elapsed_time, 3),
            "success": success,
            "response_length": response_length,
            "error": error
        }
        
        logger.info(f"LLM_METRICS: {json.dumps(metric_data)}")
    
    def log_dialog_state(self, chat_id: int, user_id: str, messages_in_history: int):
        """Логировать состояние диалога"""
        
        dialog_stats = get_dialog_stats()
        
        metric_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "dialog_state",
            "chat_id": chat_id,
            "user_id": user_id,
            "messages_in_history": messages_in_history,
            "total_dialogs": dialog_stats.get("total_dialogs", 0),
            "total_messages": dialog_stats.get("total_messages", 0)
        }
        
        logger.info(f"DIALOG_METRICS: {json.dumps(metric_data)}")
    
    def log_command_usage(self, command: str, user_id: str, chat_id: int):
        """Логировать использование команд"""
        
        metric_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "command_usage",
            "command": command,
            "user_id": user_id,
            "chat_id": chat_id
        }
        
        logger.info(f"COMMAND_METRICS: {json.dumps(metric_data)}")
    
    def log_service_suggestion(self, 
                              user_id: str, 
                              chat_id: int, 
                              user_message: str,
                              suggested_services: list,
                              services_count: int):
        """Логировать предложения услуг"""
        
        metric_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "service_suggestion",
            "user_id": user_id,
            "chat_id": chat_id,
            "user_message_length": len(user_message),
            "suggested_services": [service.get("key", "unknown") for service in suggested_services],
            "services_count": services_count
        }
        
        logger.info(f"SERVICE_METRICS: {json.dumps(metric_data)}")

# Глобальный экземпляр логгера метрик
metrics_logger = MetricsLogger()

def log_user_interaction(user_id: str, 
                        chat_id: int, 
                        message_type: str, 
                        content_length: int,
                        processing_time: Optional[float] = None):
    """
    Логировать взаимодействие пользователя
    
    Args:
        user_id: ID пользователя
        chat_id: ID чата
        message_type: Тип сообщения (text/command)
        content_length: Длина контента
        processing_time: Время обработки в секундах
    """
    interaction_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "user_interaction",
        "user_id": user_id,
        "chat_id": chat_id,
        "message_type": message_type,
        "content_length": content_length,
        "processing_time": processing_time
    }
    
    logger.info(f"USER_INTERACTION: {json.dumps(interaction_data)}")

def log_error_context(error_type: str, 
                     error_message: str,
                     user_id: str,
                     chat_id: int,
                     context: Optional[Dict[str, Any]] = None):
    """
    Логировать ошибки с контекстом
    
    Args:
        error_type: Тип ошибки
        error_message: Сообщение об ошибке
        user_id: ID пользователя
        chat_id: ID чата
        context: Дополнительный контекст
    """
    error_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "error",
        "error_type": error_type,
        "error_message": error_message,
        "user_id": user_id,
        "chat_id": chat_id,
        "context": context or {}
    }
    
    logger.error(f"ERROR_CONTEXT: {json.dumps(error_data)}")

def setup_detailed_logging():
    """Настроить детальное логирование для разных компонентов"""
    
    # Настройка форматтера для структурированных логов
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Логгер для LLM операций
    llm_logger = logging.getLogger('llm')
    llm_handler = logging.StreamHandler()
    llm_handler.setFormatter(detailed_formatter)
    llm_logger.addHandler(llm_handler)
    llm_logger.setLevel(logging.INFO)
    
    # Логгер для операций бота
    bot_logger = logging.getLogger('bot')
    bot_handler = logging.StreamHandler()
    bot_handler.setFormatter(detailed_formatter)
    bot_logger.addHandler(bot_handler)
    bot_logger.setLevel(logging.INFO)
    
    # Логгер для метрик
    metrics_logger_inst = logging.getLogger('metrics')
    metrics_handler = logging.StreamHandler()
    metrics_handler.setFormatter(detailed_formatter)
    metrics_logger_inst.addHandler(metrics_handler)
    metrics_logger_inst.setLevel(logging.INFO)
    
    logger.info("Detailed logging setup completed") 