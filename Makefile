.PHONY: build up down dev prod logs shell

build:
	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down:
	docker compose down

dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

logs:
	docker compose logs -f web

shell:
	docker compose exec -u ${UID:-1000}:${GID:-1000} bot sh