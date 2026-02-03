# ===========================================
# ScamShield - Windows Deployment Script
# ===========================================

param(
    [string]$Environment = "production"
)

Write-Host "🛡️ ScamShield Deployment Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Navigate to project root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptPath\.."

# Check for .env file
if (-not (Test-Path "backend\.env")) {
    Write-Host "No .env file found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "Please edit backend\.env with your actual values!" -ForegroundColor Red
    exit 1
}

if ($Environment -eq "development" -or $Environment -eq "dev") {
    Write-Host "Starting development environment..." -ForegroundColor Green
    docker-compose -f docker-compose.dev.yml up --build -d
    Write-Host "Development environment is running!" -ForegroundColor Green
    Write-Host "  - API: http://localhost:8000"
    Write-Host "  - API Docs: http://localhost:8000/docs"
    Write-Host "  - MongoDB UI: http://localhost:8081"
} else {
    Write-Host "Starting production environment..." -ForegroundColor Green
    
    # Check for SSL certificates
    if (-not (Test-Path "ssl\fullchain.pem") -or -not (Test-Path "ssl\privkey.pem")) {
        Write-Host "SSL certificates not found in ssl\ directory." -ForegroundColor Yellow
        Write-Host "For production, you need valid SSL certificates."
    }
    
    docker-compose up --build -d
    Write-Host "Production environment is running!" -ForegroundColor Green
    Write-Host "  - Website: https://scamshield.io"
    Write-Host "  - API: https://scamshield.io/api"
}

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Run 'docker-compose logs -f' to view logs"
