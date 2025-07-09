# Telegram Bot with LLM Integration

Telegram-бот с интеграцией LLM для консультирования пользователей.

## Требования

- Python 3.10+
- uv (для управления зависимостями)
- Токен Telegram-бота (получить у [@BotFather](https://t.me/BotFather))

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd telegram-llm-bot
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
TELEGRAM_TOKEN=your_bot_token_here
LOG_LEVEL=INFO
```

## Запуск

```bash
uv run python main.py
```

## Тестирование

```bash
uv run pytest
```

## Структура проекта

- `main.py` - точка входа приложения
- `config.py` - модуль конфигурации
- `bot/` - логика Telegram-бота
- `llm/` - модули для работы с LLM (будут реализованы в следующих итерациях)
- `test/` - тесты

## Статус разработки

- ✅ Итерация 1: Базовый Telegram-бот
- ⏳ Итерация 2: Интеграция с LLM
- ⏳ Итерация 3: Управление диалогом
- ⏳ Итерация 4: Доработка и оптимизация
- ⏳ Итерация 5: Деплой и финальное тестирование