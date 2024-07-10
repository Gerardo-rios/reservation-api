.PHONY: build up down logs shell test clean lint typecheck format db-rebuild mysql-cli db-dump db-restore

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
	docker compose -f $(COMPOSE_FILE) run --rm app black src/

lint:
	docker compose -f $(COMPOSE_FILE) run --rm app flake8 src/ --exclude __init__.py

typecheck:
	docker compose -f $(COMPOSE_FILE) run --rm app mypy src/

check:
	docker compose -f $(COMPOSE_FILE) run --rm app sh -c "flake8 src/ --exclude __init__.py && mypy src && black src"

db-rebuild:
	docker compose exec mysql mysql -uuser -ppassword -e "DROP DATABASE IF EXISTS fields_app_db; CREATE DATABASE fields_app_db;"
	docker compose exec mysql mysql -uuser -ppassword fields_app_db < db/mysql/mysql-init/init.sql

mysql-cli:
	docker compose exec mysql mysql -uuser -ppassword fields_app_db

db-dump:
	docker compose exec mysql sh -c 'exec mysqldump -uuser -ppassword fields_app_db' > db/mysql/mysql-dump/fields_app_db.sql

db-restore:
	docker compose exec -T mysql mysql -uuser -ppassword fields_app_db < db/mysql/mysql-dump/fields_app_db.sql