.PHONY: build up down logs shell test clean format db-rebuild mysql-cli db-dump db-restore check-python-version init

COMPOSE_FILE := docker-compose.yml

build:
	docker compose -f $(COMPOSE_FILE) build

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

shell:
	docker compose -f $(COMPOSE_FILE) exec app /bin/bash

test:
	docker compose -f $(COMPOSE_FILE) run --rm app pytest src/

clean:
	docker compose -f $(COMPOSE_FILE) down -v --rmi all

restart: down build up

format:
	flake8 src/ --exclude __init__.py && mypy src && black src

db-rebuild:
	docker compose exec mysql mysql -u$(DB_USER) -p$(DB_PASSWORD) -e "DROP DATABASE IF EXISTS fields_app_db; CREATE DATABASE fields_app_db;"

mysql-cli:
	docker compose exec mysql mysql -uuser -ppassword fields_app_db

db-dump:
	docker compose exec mysql sh -c 'exec mysqldump -uuser -ppassword fields_app_db' > db/mysql/mysql-dump/fields_app_db.sql

db-restore:
	docker compose exec -T mysql mysql -uuser -ppassword fields_app_db < db/mysql/mysql-dump/fields_app_db.sql

check-python-version:
	@echo "Checking python version..."
	@if [ "$(shell printf "$(PYTHON_VERSION)\n$(MIN_PYTHON_VERSION)" | sort -V | head -n1)" != "$(MIN_PYTHON_VERSION)" ]; then \
        echo "ERROR: Python 3.12.0 or higher is required. You are using $(PYTHON_VERSION)"; \
        exit 1; \
    fi

init: check-python-version
	python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry install && \
    pre-commit install

alembic-autogenerate:
	@if [ -z "$(MESSAGE)" ]; then \
		echo "Error: MESSAGE is required. Use 'make alembic-autogenerate MESSAGE=\"Your migration message\"'"; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(MESSAGE)"

alembic-upgrade:
	alembic upgrade head