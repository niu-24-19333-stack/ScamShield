# ===========================================
# ScamShield Backend
# ===========================================

FastAPI backend for ScamShield scam detection platform.

## Structure

```
app/
├── api/
│   ├── v1/              # API version 1
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── users.py     # User management
│   │   ├── scans.py     # Scan endpoints
│   │   ├── threats.py   # Threat management
│   │   ├── analytics.py # Analytics endpoints
│   │   ├── admin.py     # Admin endpoints
│   │   └── router.py    # Route aggregation
│   └── __init__.py
├── core/
│   ├── config.py        # App configuration
│   ├── security.py      # Security utilities
│   └── dependencies.py  # DI dependencies
├── db/
│   ├── mongodb.py       # MongoDB connection
│   └── models/          # Database models
├── schemas/
│   ├── auth.py          # Auth schemas
│   ├── user.py          # User schemas
│   ├── scan.py          # Scan schemas
│   └── threat.py        # Threat schemas
├── services/
│   ├── auth_service.py  # Auth logic
│   ├── user_service.py  # User logic
│   ├── scan_service.py  # Scan logic
│   └── threat_service.py # Threat logic
├── config.py            # Settings
└── main.py              # Application entry
prompts/
└── agent_prompt.txt     # AI prompts
tests/
└── test_api.py          # API tests
```

## Setup

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run server
uvicorn app.main:app --reload
```

### Docker

```bash
# Development
docker build -f Dockerfile.dev -t scamshield-api-dev .
docker run -p 8000:8000 -v $(pwd):/app scamshield-api-dev

# Production
docker build -t scamshield-api .
docker run -p 8000:8000 --env-file .env scamshield-api
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/google` - Google OAuth

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile
- `POST /api/v1/users/me/api-key` - Generate API key
- `DELETE /api/v1/users/me/api-key` - Revoke API key

### Scans
- `POST /api/v1/scans/scan` - Analyze text
- `POST /api/v1/scans/url` - Check URL
- `POST /api/v1/scans/batch` - Batch scan
- `GET /api/v1/scans/history` - Scan history

### Threats
- `GET /api/v1/threats` - List threats
- `GET /api/v1/threats/{id}` - Get threat
- `POST /api/v1/threats/report` - Report threat

### Analytics
- `GET /api/v1/analytics/stats` - Get statistics
- `GET /api/v1/analytics/trends` - Get trends

## Testing

```bash
pytest -v
pytest --cov=app  # With coverage
```

## Environment Variables

See `.env.example` for all configuration options.

Required:
- `SECRET_KEY` - Application secret
- `MONGODB_URL` - Database connection
- `GROQ_API_KEY` - Groq AI API key
- `JWT_SECRET_KEY` - JWT signing key
