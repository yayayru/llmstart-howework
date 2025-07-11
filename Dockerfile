# Упрощенный Dockerfile
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Установка зависимостей Python глобально
RUN pip install --no-cache-dir \
    aiogram>=3.0.0 \
    python-dotenv>=1.0.0 \
    openai>=1.0.0

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash --uid 1000 botuser

# Установка рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY --chown=botuser:botuser . .

# Переключение на непривилегированного пользователя
USER botuser

# Указание порта (если потребуется для healthcheck)
EXPOSE 8080

# Healthcheck для мониторинга состояния контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import config; config.get_telegram_token()" || exit 1

# Запуск приложения
CMD ["python", "main.py"] 