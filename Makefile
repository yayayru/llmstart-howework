# Makefile для автоматизации разработки Telegram-бота с LLM

# Переменные
IMAGE_NAME = telegram-llm-bot
CONTAINER_NAME = telegram-llm-bot
ENV_FILE = .env

# Проверка наличия .env файла
.PHONY: check-env
check-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "❌ Файл .env не найден. Создайте его на основе env.example:"; \
		echo "   cp env.example .env"; \
		echo "   Затем настройте переменные окружения."; \
		exit 1; \
	fi

# Установка зависимостей для разработки
.PHONY: install
install:
	@echo "📦 Установка зависимостей..."
	uv sync

# Сборка Docker образа
.PHONY: build
build:
	@echo "🔨 Сборка Docker образа..."
	docker build -t $(IMAGE_NAME) .
	@echo "✅ Образ $(IMAGE_NAME) успешно собран"

# Запуск контейнера
.PHONY: run
run: check-env
	@echo "🚀 Запуск бота в контейнере..."
	docker run -d --name $(CONTAINER_NAME) --env-file $(ENV_FILE) $(IMAGE_NAME)
	@echo "✅ Бот запущен в контейнере $(CONTAINER_NAME)"

# Запуск для разработки (локально)
.PHONY: dev
dev: check-env
	@echo "🔧 Запуск бота для разработки..."
	uv run python main.py

# Остановка контейнера
.PHONY: stop
stop:
	@echo "🛑 Остановка контейнера..."
	docker stop $(CONTAINER_NAME) || true
	@echo "✅ Контейнер остановлен"

# Просмотр логов
.PHONY: logs
logs:
	@echo "📋 Просмотр логов..."
	docker logs -f $(CONTAINER_NAME)

# Запуск тестов
.PHONY: test
test:
	@echo "🧪 Запуск тестов..."
	uv run pytest -v

# Запуск тестов с покрытием
.PHONY: test-coverage
test-coverage:
	@echo "🧪 Запуск тестов с покрытием..."
	uv run pytest -v --cov=. --cov-report=html --cov-report=term

# Линтинг кода
.PHONY: lint
lint:
	@echo "🔍 Проверка кода..."
	uv run flake8 . --exclude=.venv --max-line-length=88
	uv run black . --check --exclude=.venv

# Форматирование кода
.PHONY: format
format:
	@echo "🎨 Форматирование кода..."
	uv run black . --exclude=.venv

# Очистка (остановка и удаление контейнера и образа)
.PHONY: clean
clean:
	@echo "🧹 Очистка..."
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
	@echo "✅ Очистка завершена"

# Полная очистка (включая dangling images)
.PHONY: clean-all
clean-all: clean
	@echo "🧹 Полная очистка..."
	docker system prune -f
	@echo "✅ Полная очистка завершена"

# Перезапуск (остановка, пересборка и запуск)
.PHONY: restart
restart: stop build run

# Docker Compose команды
.PHONY: up
up: check-env
	@echo "🚀 Запуск через docker-compose..."
	docker-compose up -d
	@echo "✅ Бот запущен через docker-compose"

.PHONY: down
down:
	@echo "🛑 Остановка docker-compose..."
	docker-compose down
	@echo "✅ Docker-compose остановлен"

.PHONY: up-dev
up-dev: check-env
	@echo "🔧 Запуск в режиме разработки..."
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
	@echo "✅ Бот запущен в режиме разработки"

.PHONY: logs-compose
logs-compose:
	@echo "📋 Просмотр логов docker-compose..."
	docker-compose logs -f

# Проверка состояния контейнера
.PHONY: status
status:
	@echo "📊 Состояние контейнера:"
	docker ps -a --filter name=$(CONTAINER_NAME)

# Подключение к контейнеру
.PHONY: shell
shell:
	@echo "🐚 Подключение к контейнеру..."
	docker exec -it $(CONTAINER_NAME) /bin/bash

# Настройка окружения (копирование env.example в .env)
.PHONY: setup
setup:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "📋 Создание файла .env из шаблона..."; \
		cp env.example $(ENV_FILE); \
		echo "✅ Файл .env создан. Настройте переменные окружения."; \
	else \
		echo "⚠️  Файл .env уже существует"; \
	fi

# Помощь
.PHONY: help
help:
	@echo "📚 Доступные команды:"
	@echo ""
	@echo "  🚀 Основные команды:"
	@echo "    setup      - Создать .env файл из шаблона"
	@echo "    build      - Собрать Docker образ"
	@echo "    run        - Запустить бота в контейнере"
	@echo "    dev        - Запустить бота для разработки"
	@echo "    stop       - Остановить контейнер"
	@echo "    restart    - Перезапустить (stop + build + run)"
	@echo ""
	@echo "  🐳 Docker Compose:"
	@echo "    up         - Запустить через docker-compose"
	@echo "    down       - Остановить docker-compose"
	@echo "    up-dev     - Запустить в режиме разработки"
	@echo "    logs-compose - Просмотр логов docker-compose"
	@echo ""
	@echo "  🔧 Разработка:"
	@echo "    install    - Установить зависимости"
	@echo "    test       - Запустить тесты"
	@echo "    test-coverage - Запустить тесты с покрытием"
	@echo "    lint       - Проверить код"
	@echo "    format     - Форматировать код"
	@echo ""
	@echo "  📊 Мониторинг:"
	@echo "    logs       - Просмотр логов"
	@echo "    status     - Состояние контейнера"
	@echo "    shell      - Подключиться к контейнеру"
	@echo ""
	@echo "  🧹 Очистка:"
	@echo "    clean      - Удалить контейнер и образ"
	@echo "    clean-all  - Полная очистка системы"
	@echo ""

# Команда по умолчанию
.DEFAULT_GOAL := help 