import pytest
from unittest.mock import patch, AsyncMock, Mock
from llm.client import get_llm_response
from llm.prompts import get_system_prompt

@pytest.mark.asyncio
async def test_llm_response_success():
    """Тест успешного ответа LLM"""
    with patch('llm.client.OpenAI') as mock_openai, \
         patch('llm.client.asyncio.to_thread') as mock_to_thread:
        
        # Настраиваем мок ответа
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        # Настраиваем мок asyncio.to_thread
        mock_to_thread.return_value = mock_response
        
        # Тестируем
        messages = [{"role": "user", "content": "Test message"}]
        result = await get_llm_response(messages)
        
        assert result == "Test response"

@pytest.mark.asyncio
async def test_llm_response_timeout():
    """Тест обработки таймаута"""
    with patch('llm.client.OpenAI') as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("timeout"))
        
        messages = [{"role": "user", "content": "Test message"}]
        result = await get_llm_response(messages)
        
        assert "неожиданная ошибка" in result.lower()

@pytest.mark.asyncio 
async def test_llm_response_general_error():
    """Тест обработки общей ошибки"""
    with patch('llm.client.OpenAI') as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("General error"))
        
        messages = [{"role": "user", "content": "Test message"}]
        result = await get_llm_response(messages)
        
        assert "неожиданная ошибка" in result.lower()

def test_system_prompt():
    """Тест системного промпта"""
    prompt = get_system_prompt()
    assert "консультант" in prompt.lower()
    assert "Sign Language Interface" in prompt
    assert "жестовых технологий" in prompt 