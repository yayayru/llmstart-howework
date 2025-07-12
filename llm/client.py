import asyncio
import logging
import time
from openai import OpenAI, APIError, RateLimitError, APITimeoutError
from typing import List, Dict, Optional
from config import get_openrouter_api_key, get_llm_model, get_llm_timeout

logger = logging.getLogger(__name__)

# Настройки повторных попыток
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # секунды

async def get_llm_response(messages: List[Dict[str, str]], max_retries: int = MAX_RETRIES) -> str:
    """
    Получить ответ от LLM через OpenRouter API с поддержкой повторных попыток
    
    Args:
        messages: Список сообщений в формате [{"role": "user", "content": "..."}]
        max_retries: Максимальное количество повторных попыток
    
    Returns:
        Ответ от LLM
    """
    start_time = time.time()
    
    # Логируем только в первый раз, до цикла попыток
    model = get_llm_model()
    timeout = get_llm_timeout()
    
    logger.info(f"🔄 LLM REQUEST | Model: {model} | Messages: {len(messages)}")
    
    # Логируем системный промпт и последние сообщения только один раз
    if messages:
        system_msg = messages[0] if messages[0].get('role') == 'system' else None
        if system_msg:
            logger.info(f"🤖 System prompt: {system_msg['content'][:200]}...")
        
        # Логируем последние пользовательские сообщения
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        if user_messages:
            last_user_msg = user_messages[-1]['content']
            logger.info(f"👤 Last user message: {last_user_msg}")
    
    for attempt in range(max_retries + 1):
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=get_openrouter_api_key()
            )
            
            if attempt > 0:
                logger.info(f"🔄 LLM RETRY | Attempt: {attempt + 1}/{max_retries + 1}")
            
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=messages,
                timeout=timeout
            )
            
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=messages,
                timeout=timeout
            )
            
            if not response.choices or len(response.choices) == 0:
                raise APIError("No choices returned from LLM API")
            
            result = response.choices[0].message.content
            if not result:
                raise APIError("Empty content returned from LLM API")
            
            elapsed_time = time.time() - start_time
            logger.info(f"✅ LLM RESPONSE | Success | Length: {len(result)} chars | Time: {elapsed_time:.2f}s")
            logger.info(f"🎯 LLM Content: {result}")
            
            return result
            
        except APITimeoutError as e:
            logger.warning(f"LLM request timeout on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))  # Экспоненциальная задержка
                continue
            logger.error("LLM request timeout after all retries")
            return "Извините, сервис временно недоступен из-за превышения времени ожидания. Попробуйте позже или обратитесь к техническим специалистам."
            
        except RateLimitError as e:
            logger.warning(f"LLM rate limit exceeded on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries:
                await asyncio.sleep(RETRY_DELAY * (attempt + 2))  # Больше задержка для rate limit
                continue
            logger.error("LLM rate limit exceeded after all retries")
            return "Слишком много запросов к сервису. Пожалуйста, попробуйте через несколько минут."
            
        except APIError as e:
            error_message = str(e).lower()
            logger.warning(f"LLM API error on attempt {attempt + 1}: {str(e)}")
            
            # Проверяем, стоит ли повторять попытку для данной ошибки
            if any(keyword in error_message for keyword in ["temporary", "unavailable", "502", "503", "504"]):
                if attempt < max_retries:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                    continue
            
            logger.error(f"LLM API error after attempt {attempt + 1}: {str(e)}")
            if "invalid" in error_message or "unauthorized" in error_message:
                return "Ошибка конфигурации сервиса. Обратитесь к техническим специалистам."
            return "Извините, произошла ошибка сервиса. Попробуйте еще раз или обратитесь к техническим специалистам."
            
        except Exception as e:
            logger.error(f"Unexpected LLM error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                continue
            logger.error(f"Unexpected LLM error after all retries: {str(e)}")
            return "Произошла неожиданная ошибка. Попробуйте еще раз или обратитесь к техническим специалистам."

async def validate_messages(messages: List[Dict[str, str]]) -> bool:
    """
    Валидация сообщений перед отправкой в LLM
    
    Args:
        messages: Список сообщений для валидации
        
    Returns:
        True если сообщения валидны
    """
    if not messages or len(messages) == 0:
        logger.error("Empty messages list provided to LLM")
        return False
    
    for i, message in enumerate(messages):
        if not isinstance(message, dict):
            logger.error(f"Message {i} is not a dictionary: {type(message)}")
            return False
        
        if "role" not in message or "content" not in message:
            logger.error(f"Message {i} missing required fields: {message.keys()}")
            return False
        
        if message["role"] not in ["system", "user", "assistant"]:
            logger.error(f"Message {i} has invalid role: {message['role']}")
            return False
        
        if not message["content"] or len(message["content"].strip()) == 0:
            logger.error(f"Message {i} has empty content")
            return False
    
    return True

def get_fallback_response(user_message: str = "") -> str:
    """
    Получить резервный ответ при недоступности LLM
    
    Args:
        user_message: Сообщение пользователя для контекстного ответа
        
    Returns:
        Резервный ответ
    """
    user_message_lower = user_message.lower() if user_message else ""
    
    # Простые эвристики для резервных ответов
    if any(keyword in user_message_lower for keyword in ["поиск", "найти", "словарь"]):
        return ("К сожалению, сервис временно недоступен. Для информации о нашей поисковой системе "
                "жестового языка, пожалуйста, посетите https://ods.ai/projects/sli или попробуйте позже.")
    
    if any(keyword in user_message_lower for keyword in ["обучение", "курс", "изучение"]):
        return ("К сожалению, сервис временно недоступен. Для информации о наших обучающих программах "
                "по жестовому языку, пожалуйста, посетите https://ods.ai/projects/sli или попробуйте позже.")
    
    if any(keyword in user_message_lower for keyword in ["перевод", "переводчик"]):
        return ("К сожалению, сервис временно недоступен. Для информации о нашей системе машинного перевода "
                "жестов, пожалуйста, посетите https://ods.ai/projects/sli или попробуйте позже.")
    
    return ("К сожалению, наш ИИ-ассистент временно недоступен. Пожалуйста, попробуйте позже или "
            "посетите наш сайт https://ods.ai/projects/sli для получения информации о наших услугах. "
            "Также можете воспользоваться командой /services для просмотра доступных решений.") 