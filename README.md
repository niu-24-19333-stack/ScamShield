# ===========================================
# ScamShield
# AI-Powered Scam Detection & Prevention Platform
# ===========================================

<div align="center">
  <img src="frontend/public/assets/favicon.svg" alt="ScamShield Logo" width="120"/>
  <h1>ScamShield</h1>
  <p><strong>Protecting you from digital threats with AI-powered intelligence</strong></p>
  
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
  [![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://mongodb.com)
</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

ScamShield is a comprehensive AI-powered platform designed to detect and prevent scam attempts in real-time. Using advanced machine learning models and pattern recognition, it protects users from phishing, fraud, and social engineering attacks.

### Key Capabilities

- **Real-time Scam Detection** - Analyze messages, emails, and URLs instantly
- **AI-Powered Analysis** - Leveraging Groq and Google Gemini for intelligent threat detection
- **Multi-vector Protection** - Covers phishing, fraud, impersonation, and more
- **User Dashboard** - Comprehensive threat monitoring and analytics
- **API Access** - Integrate protection into your own applications

---

## ✨ Features

### 🔍 Detection Engine
- Text analysis for scam patterns
- URL verification and phishing detection
- Sender reputation scoring
- Behavioral pattern recognition

### 🛡️ Protection Layers
- Real-time threat blocking
- Automated alerts and notifications
- Threat intelligence database
- Historical threat analysis

### 📊 Analytics Dashboard
- Threat statistics and trends
- User activity monitoring
- API usage tracking
- Custom reports

### 🔌 Developer API
- RESTful API endpoints
- Batch processing support
- Webhook integrations
- Rate limiting and quotas

---

## 📁 Project Structure

```
scamshield/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── v1/           # API version 1
│   │   ├── core/             # Core configurations
│   │   ├── db/               # Database models & connection
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── main.py           # Application entry point
│   │   └── config.py         # Configuration
│   ├── prompts/              # AI prompts
│   ├── tests/                # Unit & integration tests
│   ├── Dockerfile            # Production Dockerfile
│   ├── Dockerfile.dev        # Development Dockerfile
│   ├── requirements.txt      # Python dependencies
│   ├── pytest.ini           # Test configuration
│   └── .env.example         # Environment template
│
├── frontend/                  # Static Frontend
│   ├── public/
│   │   ├── assets/          # Images, icons, fonts
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # JavaScript files
│   │   ├── index.html       # Landing page
│   │   ├── dashboard.html   # User dashboard
│   │   ├── login.html       # Authentication
│   │   └── ...              # Other pages
│   ├── Dockerfile           # Nginx container
│   ├── nginx.conf           # Nginx configuration
│   └── .dockerignore
│
├── docker/                   # Docker configurations
│   ├── nginx/
│   │   ├── nginx.conf       # Production Nginx
│   │   └── conf.d/
│   │       └── default.conf # Server configuration
│   └── mongo-init.js        # MongoDB initialization
│
├── scripts/                  # Deployment scripts
│   ├── deploy.sh            # Linux/Mac deployment
│   └── deploy.ps1           # Windows deployment
│
├── ssl/                      # SSL certificates (gitignored)
│   └── .gitkeep
│
├── docker-compose.yml        # Production compose
├── docker-compose.dev.yml    # Development compose
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### One-Command Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/scamshield.git
cd scamshield

# Copy environment file
cp backend/.env.example backend/.env
# Edit .env with your API keys

# Start with Docker
docker-compose up -d
```

Access the application:
- **Website**: http://localhost
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 💻 Development Setup

### Option 1: Docker Development

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run development server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend/public

# Serve with any static server
python -m http.server 5500
# or
npx serve .
```

### Running Tests

```bash
cd backend
pytest -v
```

---

## 🌐 Production Deployment

### Using Docker Compose

```bash
# Build and start services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Using Deployment Scripts

**Windows:**
```powershell
.\scripts\deploy.ps1 -Environment production
```

**Linux/Mac:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh production
```

### SSL Configuration

For HTTPS, place your SSL certificates in the `ssl/` directory:
- `fullchain.pem` - Full certificate chain
- `privkey.pem` - Private key

Or use Let's Encrypt with certbot.

---

## 📡 API Documentation

### Authentication

All API endpoints require authentication via Bearer token:

```bash
Authorization: Bearer your_api_key
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/scan` | Analyze text for scams |
| POST | `/api/v1/scan/url` | Check URL safety |
| POST | `/api/v1/scan/batch` | Batch analysis |
| GET | `/api/v1/threats/{id}` | Get threat details |
| GET | `/api/v1/stats` | Get usage statistics |
| POST | `/api/v1/report` | Report scam/false positive |

### Example Request

```bash
curl -X POST "https://api.scamshield.io/v1/scan" \
  -H "Authorization: Bearer sk_live_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"text": "You won $1,000,000! Click here to claim."}'
```

### Response

```json
{
  "status": "success",
  "is_scam": true,
  "confidence": 0.94,
  "threat_type": "lottery_scam",
  "tactics": ["urgency", "greed", "impersonation"],
  "recommendation": "Do not click. This is a common lottery scam."
}
```

Interactive API documentation available at `/docs` (Swagger UI) or `/redoc`.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Application secret key | Required |
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017/scamshield` |
| `GROQ_API_KEY` | Groq API key for AI | Required |
| `GOOGLE_API_KEY` | Google Gemini API key | Optional |
| `JWT_SECRET_KEY` | JWT signing key | Required |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000` |

See `backend/.env.example` for full configuration options.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [MongoDB](https://mongodb.com) - NoSQL database
- [Groq](https://groq.com) - AI inference API
- [Google Gemini](https://ai.google.dev) - AI models

---

<div align="center">
  <strong>Built with ❤️ for a safer internet</strong>
  <br><br>
  <a href="https://scamshield.io">Website</a> •
  <a href="https://docs.scamshield.io">Documentation</a> •
  <a href="https://github.com/yourusername/scamshield/issues">Report Bug</a>
</div>
