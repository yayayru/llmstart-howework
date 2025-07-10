"""
Модуль с услугами компании Sign Language Interface
Компания специализируется на разработке решений для распознавания жестов
"""
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Услуги компании Sign Language Interface
COMPANY_SERVICES = {
    "поисковая_система": {
        "name": "Поисковая система для жестового языка",
        "description": "Интеллектуальная поисковая система для нахождения жестов по описанию или контексту",
        "keywords": ["поиск", "жест", "словарь", "база данных", "найти", "искать"],
        "details": [
            "Поиск жестов по текстовому описанию",
            "Распознавание жестов из видео",
            "Интеграция с базой данных жестов",
            "API для сторонних приложений"
        ],
        "type": "MVP",
        "target_audience": "образовательные учреждения, сообщества глухих"
    },
    "обучающая_система": {
        "name": "Интерактивная система обучения жестовому языку",
        "description": "Комплексная платформа для изучения жестового языка с использованием ИИ",
        "keywords": ["обучение", "изучение", "курс", "учеба", "преподавание", "образование"],
        "details": [
            "Персонализированные уроки жестового языка",
            "Оценка правильности выполнения жестов",
            "Интерактивные упражнения и игры",
            "Отслеживание прогресса обучения"
        ],
        "type": "Medium VP",
        "target_audience": "студенты, преподаватели, самообучающиеся"
    },
    "машинный_перевод": {
        "name": "Система машинного перевода жестов",
        "description": "Автоматический перевод между жестовым и устным языком в реальном времени",
        "keywords": ["перевод", "переводчик", "устный", "жестовый", "коммуникация"],
        "details": [
            "Перевод с жестового языка на устный",
            "Перевод с устного языка на жестовый",
            "Работа в реальном времени",
            "Поддержка различных диалектов жестового языка"
        ],
        "type": "Maximal VP",
        "target_audience": "широкий круг пользователей, корпоративные клиенты"
    },
    "консалтинг": {
        "name": "Консультационные услуги по жестовым интерфейсам",
        "description": "Экспертная поддержка в разработке и внедрении решений для жестового интерфейса",
        "keywords": ["консультация", "экспертиза", "внедрение", "разработка", "консалтинг"],
        "details": [
            "Анализ потребностей в жестовых интерфейсах",
            "Техническая экспертиза решений",
            "Разработка стратегии внедрения",
            "Обучение команды разработчиков"
        ],
        "type": "Consulting",
        "target_audience": "IT-компании, стартапы, крупные корпорации"
    },
    "ui_ux_дизайн": {
        "name": "UI/UX дизайн для жестовых интерфейсов",
        "description": "Создание пользовательских интерфейсов, адаптированных для жестового управления",
        "keywords": ["дизайн", "интерфейс", "ui", "ux", "пользовательский", "жестовый"],
        "details": [
            "Дизайн интерфейсов для жестового управления",
            "Исследование пользовательского опыта",
            "Прототипирование жестовых интерфейсов",
            "Тестирование с реальными пользователями"
        ],
        "type": "Design",
        "target_audience": "продуктовые команды, дизайн-агентства"
    }
}

# Информация о компании
COMPANY_INFO = {
    "name": "Sign Language Interface",
    "website": "https://ods.ai/projects/sli",
    "description": "Компания специализируется на разработке передовых решений для распознавания жестов и создания доступных технологий для жестового языка",
    "mission": "Улучшение доступности технологий для людей, использующих жестовые языки"
}

def get_company_info() -> Dict:
    """Получить информацию о компании"""
    return COMPANY_INFO

def get_all_services() -> Dict[str, Dict]:
    """Получить все услуги компании"""
    return COMPANY_SERVICES

def find_relevant_services(user_message: str) -> List[Dict]:
    """
    Найти релевантные услуги на основе сообщения пользователя
    
    Args:
        user_message: Сообщение пользователя
        
    Returns:
        Список релевантных услуг
    """
    user_message_lower = user_message.lower()
    relevant_services = []
    
    for service_key, service_info in COMPANY_SERVICES.items():
        # Проверяем совпадение по ключевым словам
        keywords_match = any(keyword in user_message_lower for keyword in service_info["keywords"])
        
        if keywords_match:
            relevant_services.append({
                "key": service_key,
                "name": service_info["name"],
                "description": service_info["description"],
                "details": service_info["details"],
                "type": service_info["type"],
                "target_audience": service_info["target_audience"]
            })
    
    logger.info(f"Found {len(relevant_services)} relevant services for message: {user_message}")
    return relevant_services

def get_service_details(service_key: str) -> Optional[Dict]:
    """
    Получить подробную информацию об услуге
    
    Args:
        service_key: Ключ услуги
        
    Returns:
        Информация об услуге или None
    """
    return COMPANY_SERVICES.get(service_key)

def format_services_for_prompt(services: List[Dict]) -> str:
    """
    Форматировать услуги для включения в промпт
    
    Args:
        services: Список услуг
        
    Returns:
        Отформатированная строка для промпта
    """
    if not services:
        return "Подходящие услуги не найдены."
    
    formatted = "Релевантные услуги компании:\n"
    
    for service in services:
        formatted += f"• {service['name']}: {service['description']}\n"
        formatted += f"  Тип: {service['type']}\n"
        formatted += f"  Целевая аудитория: {service['target_audience']}\n"
    
    return formatted 