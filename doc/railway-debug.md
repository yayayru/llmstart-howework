# 🔍 Глубокая диагностика проблем Railway

## Проблема: Переменные добавлены, редеплой выполнен, но ошибка остается

Если базовые шаги не помогли, нужна более глубокая диагностика.

## Шаг 1: Детальная проверка переменных в Railway

### 1.1 Откройте Variables и сделайте скриншот

1. Railway Dashboard → Ваш проект → Сервис → **Variables**
2. Убедитесь, что видите **ТОЧНО** эти 5 переменных:

```
TELEGRAM_BOT_TOKEN
OPENROUTER_API_KEY  
LLM_MODEL
LLM_TIMEOUT
LOG_LEVEL
```

### 1.2 Проверьте значения переменных

**TELEGRAM_BOT_TOKEN** должен выглядеть как:
```
7759276891:AAH2q8IerPdO85_HflvDkftItcMbwRkiigI
```
(начинается с цифр, содержит двоеточие и длинную строку)

**OPENROUTER_API_KEY** должен выглядеть как:
```
sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
(начинается с "sk-or-v1-")

## Шаг 2: Проверка через Railway CLI

### 2.1 Установка Railway CLI

```bash
npm install -g @railway/cli
```

### 2.2 Подключение к проекту

```bash
# Логин
railway login

# Связывание с проектом
railway link
```

### 2.3 Проверка переменных через CLI

```bash
# Просмотр всех переменных
railway variables

# Должны увидеть что-то типа:
# TELEGRAM_BOT_TOKEN=7759276891:AAH...
# OPENROUTER_API_KEY=sk-or-v1-...
# LLM_MODEL=anthropic/claude-3-haiku
# LLM_TIMEOUT=30
# LOG_LEVEL=INFO
```

### 2.4 Принудительная установка переменных через CLI

```bash
railway variables set TELEGRAM_BOT_TOKEN="ваш_токен_здесь"
railway variables set OPENROUTER_API_KEY="ваш_ключ_здесь"
railway variables set LLM_MODEL="anthropic/claude-3-haiku"
railway variables set LLM_TIMEOUT="30"
railway variables set LOG_LEVEL="INFO"
```

### 2.5 Принудительный редеплой через CLI

```bash
railway up --detach
```

## Шаг 3: Альтернативный подход - Railway с railway.toml

### 3.1 Создание файла railway.toml

Создайте файл `railway.toml` в корне проекта:

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
numReplicas = 1
sleepApplication = false
restartPolicyType = "ON_FAILURE"
```

### 3.2 Коммит и пуш

```bash
git add railway.toml
git commit -m "Add railway.toml configuration"
git push origin main
```

## Шаг 4: Проверка образа Docker локально

### 4.1 Тест с переменными локально

```bash
# Сборка образа
docker build -t test-bot .

# Запуск с переменными (замените на ваши реальные значения)
docker run -e TELEGRAM_BOT_TOKEN="ваш_токен" \
           -e OPENROUTER_API_KEY="ваш_ключ" \
           -e LLM_MODEL="anthropic/claude-3-haiku" \
           -e LLM_TIMEOUT="30" \
           -e LOG_LEVEL="INFO" \
           test-bot
```

Если локально работает, проблема в Railway. Если не работает - проблема в коде.

## Шаг 5: Диагностика логов Railway

### 5.1 Поиск конкретных ошибок

В логах Railway ищите:

**Хорошие признаки:**
```
Detailed logging setup completed
Starting bot...
Start polling
```

**Плохие признаки:**
```
TELEGRAM_BOT_TOKEN not found
ValueError: TELEGRAM_BOT_TOKEN not found
ModuleNotFoundError
```

### 5.2 Время логов

Убедитесь, что смотрите **НОВЫЕ** логи после последнего редеплоя, а не старые.

## Шаг 6: Альтернатива - Render.com

Если Railway не работает, попробуйте Render:

### 6.1 Регистрация в Render

1. Откройте [render.com](https://render.com)
2. Зарегистрируйтесь через GitHub

### 6.2 Создание Web Service

1. **New** → **Web Service**
2. Подключите GitHub репозиторий
3. Настройки:
   - **Name**: telegram-llm-bot
   - **Language**: Docker
   - **Branch**: main
   - **Build Command**: (оставить пустым)
   - **Start Command**: (оставить пустым)

### 6.3 Переменные окружения в Render

В разделе **Environment Variables** добавьте:
```
TELEGRAM_BOT_TOKEN = ваш_токен
OPENROUTER_API_KEY = ваш_ключ
LLM_MODEL = anthropic/claude-3-haiku
LLM_TIMEOUT = 30
LOG_LEVEL = INFO
```

## Шаг 7: Диагностика токенов

### 7.1 Проверка Telegram токена

1. Откройте Telegram → @BotFather
2. Отправьте `/mybots`
3. Выберите бота → **API Token**
4. Скопируйте токен ПОЛНОСТЬЮ

### 7.2 Тест токена через curl

```bash
curl -X GET "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getMe"
```

Должен вернуть информацию о боте.

### 7.3 Проверка OpenRouter ключа

```bash
curl -X GET "https://openrouter.ai/api/v1/models" \
     -H "Authorization: Bearer <ВАШ_КЛЮЧ>"
```

Должен вернуть список моделей.

## Шаг 8: Экстренный вариант - Упрощенная версия

### 8.1 Создание минимального Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка только необходимого
RUN pip install aiogram python-dotenv openai

# Копирование только main.py и config.py
COPY main.py config.py ./
COPY bot/ ./bot/
COPY llm/ ./llm/

# Запуск от root (временно)
CMD ["python", "main.py"]
```

### 8.2 Пуш упрощенной версии

```bash
git add Dockerfile
git commit -m "Simplified Dockerfile for debugging"
git push origin main
```

## Результат диагностики

**Выполните шаги и сообщите:**

1. ✅ Что показывает `railway variables`?
2. ✅ Какие ТОЧНО логи показывает Railway после редеплоя?
3. ✅ Работает ли Docker образ локально?
4. ✅ Возвращает ли curl информацию о боте?

**После этого мы точно найдем проблему!** 🔍 