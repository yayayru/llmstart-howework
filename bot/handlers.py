import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from llm.client import get_llm_response
from llm.prompts import get_system_prompt, get_base_system_prompt
from llm.memory import add_message_to_dialog, get_dialog_history, clear_dialog_history
from llm.services import get_all_services, get_company_info

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    """Обработчик команды /start"""
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Start command from user {user_id} in chat {chat_id}")
    
    # Очищаем историю диалога при старте
    clear_dialog_history(chat_id)
    
    company_info = get_company_info()
    company_name = company_info.get('name', 'Sign Language Interface')
    
    welcome_message = "👋 Добро пожаловать в " + company_name + "!\n\n"
    welcome_message += "Я — ваш консультант по решениям в области жестового языка и распознавания жестов. "
    welcome_message += "Наша компания специализируется на создании доступных технологий для людей, использующих жестовые языки.\n\n"
    welcome_message += "🔧 **Доступные команды:**\n"
    welcome_message += "/services — Посмотреть все наши услуги\n"
    welcome_message += "/help — Справка по использованию бота\n"
    welcome_message += "/contact — Контактная информация\n\n"
    welcome_message += "💬 **Как начать:**\n"
    welcome_message += "Просто опишите вашу задачу или проект, и я помогу подобрать подходящие решения из нашего портфеля услуг.\n\n"
    welcome_message += "Расскажите, что вас интересует в области жестовых технологий?"
    
    # Сохраняем приветственное сообщение в историю
    add_message_to_dialog(chat_id, "assistant", welcome_message)
    
    await message.answer(welcome_message)

async def cmd_services(message: Message):
    """Обработчик команды /services"""
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Services command from user {user_id} in chat {chat_id}")
    
    services = get_all_services()
    company_info = get_company_info()
    company_name = company_info.get('name', 'Sign Language Interface')
    
    services_message = "🚀 **Услуги " + company_name + "**\n\n"
    
    for service_key, service_info in services.items():
        services_message += "**" + service_info['name'] + "** (" + service_info['type'] + ")\n"
        services_message += "📝 " + service_info['description'] + "\n"
        services_message += "👥 Для: " + service_info['target_audience'] + "\n\n"
    
    website = company_info.get('website', '')
    services_message += "💡 Подробнее: " + website + "\n"
    services_message += "💬 Напишите мне о вашем проекте, и я подберу подходящие решения!"
    
    # Сохраняем в историю
    add_message_to_dialog(chat_id, "user", "/services")
    add_message_to_dialog(chat_id, "assistant", services_message)
    
    await message.answer(services_message)

async def cmd_help(message: Message):
    """Обработчик команды /help"""
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Help command from user {user_id} in chat {chat_id}")
    
    help_message = "📖 **Справка по использованию бота**\n\n"
    help_message += "🤖 **Что я умею:**\n"
    help_message += "• Консультировать по услугам в области жестовых технологий\n"
    help_message += "• Подбирать подходящие решения под ваш проект\n"
    help_message += "• Отвечать на вопросы о наших продуктах\n"
    help_message += "• Помогать с техническими вопросами\n\n"
    help_message += "📋 **Доступные команды:**\n"
    help_message += "/start — Начать сначала\n"
    help_message += "/services — Показать все услуги\n"
    help_message += "/help — Эта справка\n"
    help_message += "/contact — Контактная информация\n\n"
    help_message += "💡 **Как общаться:**\n"
    help_message += "Просто задавайте вопросы обычным языком! Например:\n"
    help_message += "• \"Нужна система для распознавания жестов\"\n"
    help_message += "• \"Хочу обучить команду жестовому языку\"\n"
    help_message += "• \"Интересует перевод с жестового на устный язык\"\n\n"
    help_message += "Я запоминаю контекст нашего разговора и могу отвечать на уточняющие вопросы."
    
    # Сохраняем в историю
    add_message_to_dialog(chat_id, "user", "/help")
    add_message_to_dialog(chat_id, "assistant", help_message)
    
    await message.answer(help_message)

async def cmd_contact(message: Message):
    """Обработчик команды /contact"""
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info(f"Contact command from user {user_id} in chat {chat_id}")
    
    company_info = get_company_info()
    company_name = company_info.get('name', 'Sign Language Interface')
    website = company_info.get('website', '')
    mission = company_info.get('mission', '')
    
    contact_message = "📞 **Контактная информация**\n\n"
    contact_message += "🏢 **" + company_name + "**\n"
    contact_message += "🌐 Веб-сайт: " + website + "\n\n"
    contact_message += "🎯 **Наша миссия:**\n"
    contact_message += mission + "\n\n"
    contact_message += "📧 **Для деловых предложений:**\n"
    contact_message += "Если вы хотите обсудить проект детально или получить коммерческое предложение, "
    contact_message += "рекомендую связаться с нашей командой через официальный сайт.\n\n"
    contact_message += "💬 **Продолжить в чате:**\n"
    contact_message += "Я всегда готов ответить на ваши вопросы прямо здесь!"
    
    # Сохраняем в историю
    add_message_to_dialog(chat_id, "user", "/contact")
    add_message_to_dialog(chat_id, "assistant", contact_message)
    
    await message.answer(contact_message)

async def handle_message(message: Message):
    """Обработчик текстовых сообщений через LLM с сохранением контекста"""
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else "unknown"
        user_message = message.text
        
        logger.info(f"Message from user {user_id} in chat {chat_id}: {user_message}")
        
        # Добавляем сообщение пользователя в историю
        add_message_to_dialog(chat_id, "user", user_message)
        
        # Получаем историю диалога (последние 10 сообщений)
        history = get_dialog_history(chat_id, max_messages=10)
        
        # Формируем динамический системный промпт с учетом сообщения пользователя
        system_prompt = get_system_prompt(user_message)
        
        # Формируем запрос к LLM с динамическим системным промптом и историей
        messages = [{"role": "system", "content": system_prompt}] + history
        
        logger.info(f"Sending {len(messages)} messages to LLM (including dynamic system prompt)")
        
        # Получаем ответ от LLM
        response = await get_llm_response(messages)
        
        # Сохраняем ответ в историю
        add_message_to_dialog(chat_id, "assistant", response)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Response sent to user {user_id} in chat {chat_id}")
        
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await message.answer("Извините, произошла ошибка. Попробуйте еще раз.")

def setup_handlers(dp: Dispatcher):
    """Настройка обработчиков сообщений"""
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_services, Command("services"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_contact, Command("contact"))
    dp.message.register(handle_message) 