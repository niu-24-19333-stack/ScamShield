# ===========================================
# ScamShield - Makefile for Common Tasks
# ===========================================

.PHONY: help install dev prod test clean logs

# Default target
help:
	@echo "ScamShield - Available Commands"
	@echo "================================"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Start development environment"
	@echo "  make prod       - Start production environment"
	@echo "  make test       - Run tests"
	@echo "  make logs       - View logs"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make build      - Build Docker images"

# Install dependencies locally
install:
	cd backend && pip install -r requirements.txt

# Development
dev:
	docker-compose -f docker-compose.dev.yml up -d

# Production
prod:
	docker-compose up -d --build

# Build images
build:
	docker-compose build

# Run tests
test:
	cd backend && pytest -v

# View logs
logs:
	docker-compose logs -f

# Clean up
clean:
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

# Stop all
stop:
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

# Restart
restart:
	docker-compose restart

# Shell into backend container
shell:
	docker-compose exec backend /bin/bash
