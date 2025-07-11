# Руководство по развертыванию Telegram-бота с LLM

## Обзор

Этот документ описывает процесс развертывания и использования Telegram-бота с интеграцией LLM для компании Sign Language Interface.

## Требования

### Системные требования
- Docker >= 20.10
- Docker Compose >= 1.29
- Make (для автоматизации)
- Git

### Учетные данные
- Токен Telegram-бота (получить у @BotFather)
- API-ключ OpenRouter (https://openrouter.ai)

## Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd llmstart-howework
```

### 2. Настройка окружения
```bash
# Создание .env файла из шаблона
make setup

# Редактирование .env файла
nano .env
```

### 3. Запуск бота
```bash
# Сборка и запуск в продакшен режиме
make build
make up

# Или одной командой
make restart
```

## Настройка переменных окружения

Отредактируйте файл `.env`:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Configuration
LLM_MODEL=anthropic/claude-3-haiku
LLM_TIMEOUT=30

# Logging Configuration
LOG_LEVEL=INFO
```

## Доступные команды

### Основные команды
- `make setup` - Создать .env файл из шаблона
- `make build` - Собрать Docker образ
- `make up` - Запустить бота через docker-compose
- `make down` - Остановить docker-compose
- `make restart` - Перезапустить (stop + build + up)

### Команды для разработки
- `make install` - Установить зависимости
- `make dev` - Запустить бота для разработки (локально)
- `make up-dev` - Запустить в режиме разработки
- `make test` - Запустить тесты
- `make test-coverage` - Запустить тесты с покрытием

### Мониторинг
- `make logs` - Просмотр логов (docker run)
- `make logs-compose` - Просмотр логов (docker-compose)
- `make status` - Состояние контейнера
- `make shell` - Подключиться к контейнеру

### Очистка
- `make clean` - Удалить контейнер и образ
- `make clean-all` - Полная очистка системы

## Режимы развертывания

### Продакшен
```bash
# Сборка и запуск
make build
make up

# Мониторинг
make logs-compose
make status
```

### Разработка
```bash
# Запуск с live reload
make up-dev

# Или локально
make dev
```

## Мониторинг и логирование

### Просмотр логов
```bash
# Последние 50 строк
make logs-compose

# Следить за логами в реальном времени
docker-compose logs -f
```

### Проверка состояния
```bash
# Статус контейнера
make status

# Healthcheck
docker-compose ps
```

### Структура логов
Логи включают:
- Запросы к LLM API
- Взаимодействие с пользователями
- Ошибки и предупреждения
- Метрики производительности

## Устранение неполадок

### Проблемы с запуском

**Ошибка: "TELEGRAM_BOT_TOKEN not found"**
```bash
# Проверьте .env файл
cat .env
# Убедитесь, что токен корректный
```

**Ошибка: "Module not found"**
```bash
# Пересоберите образ
make clean
make build
```

### Проблемы с сетью

**Ошибка подключения к OpenRouter**
```bash
# Проверьте API-ключ
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     https://openrouter.ai/api/v1/models

# Проверьте сеть контейнера
docker network ls
```

### Проблемы с производительностью

**Высокое потребление памяти**
```bash
# Проверьте использование ресурсов
docker stats telegram-llm-bot

# Настройте лимиты в docker-compose.yml
```

## Безопасность

### Рекомендации
1. **Не коммитьте .env файл** - он содержит секретные ключи
2. **Используйте сильные API-ключи** - регулярно обновляйте
3. **Ограничьте доступ** - используйте firewalls и VPN
4. **Мониторьте логи** - отслеживайте подозрительную активность

### Настройка HTTPS (для продакшена)
```bash
# Используйте reverse proxy (nginx/traefik)
# Настройте SSL сертификаты
# Обновите docker-compose.yml
```

## Масштабирование

### Горизонтальное масштабирование
```yaml
# docker-compose.yml
version: '3.8'
services:
  telegram-bot:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
```

### Вертикальное масштабирование
```yaml
# Увеличьте лимиты ресурсов
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 1G
```

## Резервное копирование

### Данные для резервного копирования
- Конфигурационные файлы
- Логи (при необходимости)
- Переменные окружения

### Автоматическое резервное копирование
```bash
# Создайте скрипт для резервного копирования
#!/bin/bash
docker-compose exec telegram-bot tar -czf /backup/config-$(date +%Y%m%d).tar.gz /app
```

## Обновления

### Обновление кода
```bash
# Получить последние изменения
git pull origin main

# Пересобрать и перезапустить
make restart
```

### Обновление зависимостей
```bash
# Обновить uv.lock
uv lock --upgrade

# Пересобрать образ
make clean
make build
```

## Поддержка

### Логи отладки
```bash
# Включить детальное логирование
export LOG_LEVEL=DEBUG
make restart

# Просмотр детальных логов
make logs-compose
```

### Контакты
- **Разработчик**: dev@example.com
- **Репозиторий**: https://github.com/example/telegram-llm-bot
- **Документация**: https://docs.example.com

## Лицензия

MIT License - см. файл LICENSE в корне проекта. 