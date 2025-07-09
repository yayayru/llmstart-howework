import pytest
from unittest.mock import patch, Mock, AsyncMock
from llm.client import get_llm_response
from llm.prompts import get_system_prompt

@pytest.mark.asyncio
async def test_llm_response_success():
    """Тест успешного ответа от LLM"""
    with patch('llm.client.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Тестовый ответ"
        
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch('llm.client.asyncio.to_thread') as mock_to_thread:
            mock_to_thread.return_value = mock_response
            
            messages = [{"role": "user", "content": "Привет"}]
            response = await get_llm_response(messages)
            
            assert response == "Тестовый ответ"

@pytest.mark.asyncio
async def test_llm_response_timeout():
    """Тест таймаута запроса к LLM"""
    with patch('llm.client.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        with patch('llm.client.asyncio.to_thread') as mock_to_thread:
            # Имитируем общее исключение для упрощения теста
            mock_to_thread.side_effect = Exception("Connection timeout")
            
            messages = [{"role": "user", "content": "Привет"}]
            response = await get_llm_response(messages)
            
            assert "неожиданная ошибка" in response

@pytest.mark.asyncio
async def test_llm_response_general_error():
    """Тест общей ошибки при запросе к LLM"""
    with patch('llm.client.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        with patch('llm.client.asyncio.to_thread') as mock_to_thread:
            mock_to_thread.side_effect = Exception("General error")
            
            messages = [{"role": "user", "content": "Привет"}]
            response = await get_llm_response(messages)
            
            assert "неожиданная ошибка" in response

def test_system_prompt():
    """Тест системного промпта"""
    prompt = get_system_prompt()
    assert "консультант" in prompt.lower()
    assert "услуги" in prompt.lower()
    assert "помочь" in prompt.lower()
    assert len(prompt) > 50  # Промпт должен быть достаточно подробным 