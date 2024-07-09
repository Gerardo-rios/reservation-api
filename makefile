.PHONY: build up down logs shell test clean

COMPOSE_FILE := docker-compose.yml

IMAGE_NAME := fields-app

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
	docker compose -f $(COMPOSE_FILE) run --rm app pytest

clean:
	docker compose -f $(COMPOSE_FILE) down -v --rmi all

restart: down build up

format:
	docker compose -f $(COMPOSE_FILE) run --rm app black .

lint:
	docker compose -f $(COMPOSE_FILE) run --rm app flake8 .

type-check:
	docker compose -f $(COMPOSE_FILE) run --rm app mypy .

run:
	docker run -d -p 8000:8000 --name fields-api-container fields-api