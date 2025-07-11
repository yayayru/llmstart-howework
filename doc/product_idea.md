# ИИ-ассистент для первичной консультации клиентов

## Описание проекта

Разработка Telegram-бота на базе LLM для проведения первичной консультации клиентов компании. Бот будет автоматически обрабатывать запросы клиентов, уточнять их потребности и предлагать соответствующие услуги компании.

## Основные функции

### 1. Первичная консультация
- Обработка входящих сообщений от клиентов
- Анализ потребностей и проблем клиента
- Предоставление релевантной информации о услугах

### 2. Уточнение потребностей
- Задавание уточняющих вопросов
- Сбор детальной информации о проблеме клиента
- Определение приоритетов и ограничений

### 3. Рекомендация услуг
- Предложение подходящих услуг компании
- Объяснение преимуществ и особенностей услуг
- Перенаправление к специалистам при необходимости

## Техническая реализация

### Архитектура
- Telegram Bot API для взаимодействия с пользователями
- LLM (например, GPT-4 или аналогичный) для обработки диалогов
- Системный промпт с информацией о компании и услугах
- База данных не предусмотрена (история будет храниться в памяти)