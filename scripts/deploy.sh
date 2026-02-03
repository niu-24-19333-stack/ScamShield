#!/bin/bash
# ===========================================
# ScamShield - Deployment Script
# ===========================================

set -e

echo "🛡️ ScamShield Deployment Script"
echo "================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Parse arguments
ENVIRONMENT=${1:-production}

echo -e "${YELLOW}Deploying in ${ENVIRONMENT} mode...${NC}"

# Navigate to project root
cd "$(dirname "$0")/.."

# Check for .env file
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}No .env file found. Copying from .env.example...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${RED}Please edit backend/.env with your actual values!${NC}"
    exit 1
fi

if [ "$ENVIRONMENT" = "development" ] || [ "$ENVIRONMENT" = "dev" ]; then
    echo -e "${GREEN}Starting development environment...${NC}"
    docker-compose -f docker-compose.dev.yml up --build -d
    echo -e "${GREEN}Development environment is running!${NC}"
    echo "  - API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - MongoDB UI: http://localhost:8081"
else
    echo -e "${GREEN}Starting production environment...${NC}"
    
    # Check for SSL certificates
    if [ ! -f "ssl/fullchain.pem" ] || [ ! -f "ssl/privkey.pem" ]; then
        echo -e "${YELLOW}SSL certificates not found in ssl/ directory.${NC}"
        echo "For production, you need valid SSL certificates."
        echo "You can use Let's Encrypt or provide your own."
    fi
    
    docker-compose up --build -d
    echo -e "${GREEN}Production environment is running!${NC}"
    echo "  - Website: https://scamshield.io"
    echo "  - API: https://scamshield.io/api"
fi

echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo "Run 'docker-compose logs -f' to view logs"
