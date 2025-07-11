# Telegram Bot with LLM Integration

Профессиональный консультант компании Sign Language Interface через Telegram-бота с интеграцией LLM.

## Описание

Telegram-бот, который представляет компанию Sign Language Interface, специализирующуюся на технологиях распознавания жестов. Бот использует языковые модели через OpenRouter API для проведения профессиональной консультации. Бот может:

- Поддерживать контекст диалога (история сообщений)
- Анализировать потребности клиентов в области жестового языка
- Автоматически предлагать релевантные услуги компании
- Проводить профессиональную консультацию по жестовым технологиям
- Предоставлять информацию о 5 основных услугах компании

## Требования

- Python 3.10+
- uv (для управления зависимостями)
- Токен Telegram-бота (получить у [@BotFather](https://t.me/BotFather))
- API ключ OpenRouter (получить на [openrouter.ai](https://openrouter.ai))

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd llmstart-howework
```

2. Установите зависимости с помощью uv:
```bash
uv sync
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Заполните `.env` файл:
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Settings
LLM_MODEL=openai/gpt-4o-mini
LLM_TIMEOUT=30

# Logging Settings
LOG_LEVEL=INFO

# Company Information
COMPANY_NAME=Sign Language Interface
COMPANY_WEBSITE=https://ods.ai/projects/sli
```

## Запуск

### Локальный запуск
```bash
uv run python main.py
```

### Запуск через Docker
```bash
# Создание .env файла
make setup

# Сборка и запуск
make build
make up

# Просмотр логов
make logs-compose

# Остановка
make down
```

### Доступные команды Make
```bash
make help  # Полный список команд
```

Подробная документация по развертыванию: [doc/deployment.md](doc/deployment.md)

## Тестирование

Запуск всех тестов (25 тестов):
```bash
uv run pytest
```

Запуск конкретных тестов:
```bash
uv run pytest test/test_memory.py -v        # Тесты модуля памяти
uv run pytest test/test_llm.py -v           # Тесты LLM интеграции
uv run pytest test/test_integration.py -v   # Интеграционные тесты
```

## Структура проекта

- `main.py` - точка входа приложения
- `config.py` - модуль конфигурации
- `bot/` - логика Telegram-бота
  - `handlers.py` - обработчики сообщений и команд
- `llm/` - модули для работы с LLM
  - `client.py` - клиент для OpenRouter API
  - `memory.py` - управление историей диалогов
  - `prompts.py` - системные промпты
  - `services.py` - услуги компании Sign Language Interface
  - `logging_utils.py` - расширенное логирование и метрики
- `test/` - тесты
  - `test_integration.py` - интеграционные тесты
- `doc/` - документация

## Архитектура

Бот построен на основе функционального подхода:
- **Aiogram** - для взаимодействия с Telegram API
- **OpenRouter** - для доступа к LLM (GPT-4o-mini)
- **In-memory хранение** - история диалогов в оперативной памяти
- **Асинхронная обработка** - все операции выполняются асинхронно

## Функциональность

### Завершенные возможности:
- ✅ Базовый Telegram-бот с обработкой команд
- ✅ Интеграция с LLM через OpenRouter API
- ✅ Поддержка контекста диалога (история сообщений)
- ✅ Профессиональные промпты для консультации
- ✅ Система услуг Sign Language Interface (5 реальных услуг)
- ✅ Умное сопоставление услуг с запросами пользователей
- ✅ Новые команды: `/services`, `/help`, `/contact`
- ✅ Улучшенная обработка ошибок с повторными попытками
- ✅ Расширенное логирование и мониторинг
- ✅ Комплексное тестирование (25 тестов)
- ✅ Контейнеризация Docker + Docker Compose
- ✅ Автоматизация с Makefile
- ✅ Документация по развертыванию

## Статус разработки

- ✅ Итерация 1: Базовый Telegram-бот
- ✅ Итерация 2: Интеграция с LLM
- ✅ Итерация 3: Управление диалогом
- ✅ Итерация 4: Доработка и оптимизация
- ✅ Итерация 5: Деплой и финальное тестирование

🎉 **Проект завершен!** Все 5 итераций успешно реализованы.

## Использование

1. Запустите бота командой `uv run python main.py`
2. Найдите вашего бота в Telegram
3. Отправьте команду `/start` для начала работы
4. Используйте доступные команды:
   - `/services` - просмотр всех услуг компании
   - `/help` - подробная справка по использованию
   - `/contact` - контактная информация компании
5. Начните диалог - бот будет помнить контекст разговора и предлагать релевантные услуги

## Технические детали

- **Язык**: Python 3.12+
- **Фреймворк**: Aiogram 3.x
- **LLM**: OpenRouter API (GPT-4o-mini)
- **Тестирование**: pytest
- **Управление зависимостями**: uv
- **Принцип KISS**: минимальная архитектура без оверинжиниринга