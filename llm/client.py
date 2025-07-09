import asyncio
import logging
from openai import OpenAI, APIError, RateLimitError, APITimeoutError
from typing import List, Dict
from config import get_openrouter_api_key, get_llm_model, get_llm_timeout

logger = logging.getLogger(__name__)

async def get_llm_response(messages: List[Dict[str, str]]) -> str:
    """
    Получить ответ от LLM через OpenRouter API
    
    Args:
        messages: Список сообщений в формате [{"role": "user", "content": "..."}]
    
    Returns:
        Ответ от LLM
    """
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=get_openrouter_api_key()
        )
        
        model = get_llm_model()
        timeout = get_llm_timeout()
        
        logger.info(f"LLM request: model={model}, messages_count={len(messages)}")
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=messages,
            timeout=timeout
        )
        
        result = response.choices[0].message.content
        logger.info(f"LLM response successful: {len(result)} characters")
        return result
        
    except APITimeoutError:
        logger.error("LLM request timeout")
        return "Извините, сервис временно недоступен. Попробуйте позже."
    except RateLimitError:
        logger.error("LLM rate limit exceeded")
        return "Слишком много запросов. Попробуйте через минуту."
    except APIError as e:
        logger.error(f"LLM API error: {str(e)}")
        return "Извините, произошла ошибка сервиса. Попробуйте еще раз."
    except Exception as e:
        logger.error(f"Unexpected LLM error: {str(e)}")
        return "Произошла неожиданная ошибка. Попробуйте еще раз." 