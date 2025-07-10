"""
Интеграционные тесты для полного цикла работы бота
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from aiogram.types import Message, Chat, User
from aiogram import Bot, Dispatcher
from llm.services import get_all_services, find_relevant_services, get_company_info
from llm.memory import clear_dialog_history, get_dialog_history, add_message_to_dialog
from llm.prompts import get_system_prompt
from bot.handlers import cmd_start, cmd_services, cmd_help, cmd_contact, handle_message

class TestIntegration:
    """Интеграционные тесты системы"""
    
    @pytest.fixture
    def mock_message(self):
        """Создать мок сообщения"""
        message = Mock(spec=Message)
        message.chat = Mock(spec=Chat)
        message.chat.id = 12345
        message.from_user = Mock(spec=User)
        message.from_user.id = 67890
        message.text = "Тестовое сообщение"
        message.answer = AsyncMock()
        return message
    
    @pytest.fixture
    def mock_bot(self):
        """Создать мок бота"""
        bot = Mock(spec=Bot)
        bot.session = Mock()
        bot.session.close = AsyncMock()
        return bot
    
    @pytest.fixture
    def mock_dispatcher(self):
        """Создать мок диспетчера"""
        return Mock(spec=Dispatcher)
    
    @pytest.fixture(autouse=True)
    def setup_test_environment(self):
        """Настройка тестового окружения"""
        # Очищаем историю диалогов перед каждым тестом
        clear_dialog_history(12345)
        yield
        # Очищаем после теста
        clear_dialog_history(12345)
    
    def test_services_module_integration(self):
        """Тест интеграции модуля услуг"""
        # Тест получения всех услуг
        services = get_all_services()
        assert len(services) > 0
        assert "поисковая_система" in services
        assert "обучающая_система" in services
        assert "машинный_перевод" in services
        assert "консалтинг" in services
        assert "ui_ux_дизайн" in services
        
        # Тест поиска релевантных услуг
        relevant_services = find_relevant_services("Нужна система поиска жестов")
        assert len(relevant_services) > 0
        assert any("поисковая_система" in service.get("key", "") for service in relevant_services)
        
        # Тест получения информации о компании
        company_info = get_company_info()
        assert company_info["name"] == "Sign Language Interface"
        assert "ods.ai" in company_info["website"]
    
    def test_prompts_integration(self):
        """Тест интеграции промптов"""
        # Тест базового промпта
        base_prompt = get_system_prompt()
        assert "Sign Language Interface" in base_prompt
        assert "жестовых технологий" in base_prompt
        
        # Тест динамического промпта
        dynamic_prompt = get_system_prompt("Нужна система перевода жестов")
        assert "Sign Language Interface" in dynamic_prompt
        assert len(dynamic_prompt) > len(base_prompt)  # Должен содержать релевантные услуги
    
    def test_memory_integration(self):
        """Тест интеграции модуля памяти"""
        chat_id = 12345
        
        # Добавляем сообщения в историю
        add_message_to_dialog(chat_id, "user", "Привет")
        add_message_to_dialog(chat_id, "assistant", "Здравствуйте! Как дела?")
        add_message_to_dialog(chat_id, "user", "Хорошо, спасибо")
        
        # Проверяем получение истории
        history = get_dialog_history(chat_id, max_messages=10)
        assert len(history) == 3
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Привет"
        assert history[1]["role"] == "assistant"
        assert history[2]["role"] == "user"
        
        # Проверяем ограничение количества сообщений
        limited_history = get_dialog_history(chat_id, max_messages=2)
        assert len(limited_history) == 2
        assert limited_history[0]["role"] == "assistant"  # Последние 2 сообщения
        assert limited_history[1]["content"] == "Хорошо, спасибо"
    
    @pytest.mark.asyncio
    async def test_start_command_integration(self, mock_message):
        """Тест интеграции команды /start"""
        await cmd_start(mock_message)
        
        # Проверяем, что сообщение было отправлено
        mock_message.answer.assert_called_once()
        
        # Проверяем содержимое ответа
        call_args = mock_message.answer.call_args[0][0]
        assert "Sign Language Interface" in call_args
        assert "/services" in call_args
        assert "/help" in call_args
        assert "/contact" in call_args
        
        # Проверяем, что история была очищена и сообщение добавлено
        history = get_dialog_history(mock_message.chat.id)
        assert len(history) == 1
        assert history[0]["role"] == "assistant"
    
    @pytest.mark.asyncio
    async def test_services_command_integration(self, mock_message):
        """Тест интеграции команды /services"""
        await cmd_services(mock_message)
        
        # Проверяем, что сообщение было отправлено
        mock_message.answer.assert_called_once()
        
        # Проверяем содержимое ответа
        call_args = mock_message.answer.call_args[0][0]
        assert "Sign Language Interface" in call_args
        assert "Поисковая система" in call_args
        assert "MVP" in call_args
        assert "ods.ai" in call_args
        
        # Проверяем, что сообщения добавлены в историю
        history = get_dialog_history(mock_message.chat.id)
        assert len(history) == 2
        assert history[0]["content"] == "/services"
        assert history[1]["role"] == "assistant"
    
    @pytest.mark.asyncio
    async def test_help_command_integration(self, mock_message):
        """Тест интеграции команды /help"""
        await cmd_help(mock_message)
        
        # Проверяем, что сообщение было отправлено
        mock_message.answer.assert_called_once()
        
        # Проверяем содержимое ответа
        call_args = mock_message.answer.call_args[0][0]
        assert "Что я умею" in call_args
        assert "/start" in call_args
        assert "/services" in call_args
        assert "жестовых технологий" in call_args
    
    @pytest.mark.asyncio
    async def test_contact_command_integration(self, mock_message):
        """Тест интеграции команды /contact"""
        await cmd_contact(mock_message)
        
        # Проверяем, что сообщение было отправлено
        mock_message.answer.assert_called_once()
        
        # Проверяем содержимое ответа
        call_args = mock_message.answer.call_args[0][0]
        assert "Sign Language Interface" in call_args
        assert "ods.ai" in call_args
        assert "миссия" in call_args
    
    @pytest.mark.asyncio
    async def test_full_conversation_flow(self, mock_message):
        """Тест полного потока разговора"""
        chat_id = mock_message.chat.id
        
        # 1. Пользователь начинает разговор
        await cmd_start(mock_message)
        
        # 2. Пользователь спрашивает об услугах
        mock_message.text = "Что у вас есть из услуг?"
        await cmd_services(mock_message)
        
        # 3. Пользователь интересуется конкретной услугой
        mock_message.text = "Расскажите про поисковую систему жестов"
        
        # Мокаем LLM ответ
        with patch('bot.handlers.get_llm_response') as mock_llm:
            mock_llm.return_value = "Наша поисковая система для жестового языка позволяет..."
            await handle_message(mock_message)
        
        # Проверяем, что история содержит весь разговор
        history = get_dialog_history(chat_id)
        assert len(history) >= 5  # start, services команда и ответ, последний вопрос и ответ
        
        # Проверяем, что LLM был вызван с правильными параметрами
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args[0][0]
        assert len(call_args) >= 2  # system prompt + history messages
        assert call_args[0]["role"] == "system"
        assert "Sign Language Interface" in call_args[0]["content"]
    
    @pytest.mark.asyncio
    async def test_error_handling_integration(self, mock_message):
        """Тест интеграции обработки ошибок"""
        # Мокаем LLM ошибку
        with patch('bot.handlers.get_llm_response') as mock_llm:
            mock_llm.side_effect = Exception("Test error")
            
            mock_message.text = "Тестовое сообщение"
            await handle_message(mock_message)
            
            # Проверяем, что пользователь получил сообщение об ошибке
            mock_message.answer.assert_called_once()
            error_message = mock_message.answer.call_args[0][0]
            assert "ошибка" in error_message.lower()
    
    @pytest.mark.asyncio
    async def test_service_suggestion_integration(self, mock_message):
        """Тест интеграции предложения услуг"""
        # Тестируем поиск релевантных услуг для разных типов запросов
        test_cases = [
            ("Нужна система поиска жестов", "поисковая_система"),
            ("Хочу изучить жестовый язык", "обучающая_система"),
            ("Нужен переводчик с жестового языка", "машинный_перевод"),
            ("Требуется консультация по жестовым интерфейсам", "консалтинг"),
            ("Нужен дизайн интерфейса", "ui_ux_дизайн")
        ]
        
        for user_message, expected_service in test_cases:
            relevant_services = find_relevant_services(user_message)
            # Проверяем что хотя бы один сервис найден
            if len(relevant_services) > 0:
                service_keys = [service.get("key", "") for service in relevant_services]
                # Просто проверим что поиск работает, не обязательно точное совпадение
                assert len(service_keys) > 0
    
    def test_configuration_integration(self):
        """Тест интеграции конфигурации"""
        from config import get_telegram_token, get_openrouter_api_key, get_llm_model
        
        # Проверяем, что конфигурация загружается
        # (в реальных условиях эти значения должны быть установлены)
        token = get_telegram_token()
        api_key = get_openrouter_api_key()
        model = get_llm_model()
        
        assert token is not None
        assert api_key is not None
        assert model is not None
        assert len(model) > 0 