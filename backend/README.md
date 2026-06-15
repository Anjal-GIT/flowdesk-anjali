# Flowdesk - Shipment Management Backend API

A FastAPI-based REST API for managing shipments with PostgreSQL database integration, API key authentication, and comprehensive CRUD operations.

## Features

- ✅ **FastAPI** - Modern, fast, and intuitive API framework
- ✅ **SQLAlchemy ORM** - Powerful database toolkit
- ✅ **PostgreSQL** - Robust relational database
- ✅ **Pydantic** - Data validation using Python type hints
- ✅ **API Key Authentication** - Simple, reusable authentication dependency
- ✅ **Auto-generated Tracking Codes** - Format: `SHP-YYYYMMDD-XXXXX`
- ✅ **CORS Support** - Cross-origin resource sharing enabled
- ✅ **Interactive API Docs** - Swagger UI and ReDoc included

## Technology Stack

- **Runtime:** Python 3.8+
- **Web Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL
- **Data Validation:** Pydantic v2
- **Environment:** Python-dotenv

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database setup and session management
│   ├── models.py            # SQLAlchemy models (Shipment)
│   ├── schemas.py           # Pydantic models for validation
│   ├── dependencies.py      # Reusable dependencies (API key auth)
│   └── routers/
│       ├── __init__.py
│       └── shipments.py     # Shipment endpoints
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values
# Required variables:
# - DATABASE_URL: PostgreSQL connection string
# - API_KEY: Your API key for authentication
```

**Example .env:**
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/flowdesk
API_KEY=your-super-secret-api-key
API_TITLE=Flowdesk - Shipment Management API
API_VERSION=1.0.0
```

### 4. Setup PostgreSQL Database

```bash
# Create database (if using psql)
createdb flowdesk

# Or using SQL
psql -c "CREATE DATABASE flowdesk;"
```

### 5. Run the Application

```bash
# Development with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python app/main.py
```

The API will be available at:
- **API Base URL:** `http://localhost:8000`
- **Interactive Docs:** `http://localhost:8000/docs`
- **Alternative Docs:** `http://localhost:8000/redoc`

## API Endpoints

### Health Check

```
GET /                      - Root health check
GET /health                - Detailed health check
```

### Shipments

All endpoints require the `X-API-Key` header.

```
POST   /shipments/                           - Create a new shipment
GET    /shipments/                           - List all shipments (paginated)
GET    /shipments/{shipment_id}              - Get shipment by ID
GET    /shipments/tracking/{tracking_code}   - Get shipment by tracking code
PATCH  /shipments/{shipment_id}              - Update shipment
DELETE /shipments/{shipment_id}              - Delete shipment
```

## Usage Examples

### 1. Create a Shipment

```bash
curl -X POST "http://localhost:8000/shipments/" \
  -H "X-API-Key: your-super-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New York",
    "destination": "Los Angeles",
    "weight_kg": 25.5,
    "status": "pending"
  }'
```

**Response:**
```json
{
  "id": 1,
  "tracking_code": "SHP-20240115-ABC12",
  "origin": "New York",
  "destination": "Los Angeles",
  "weight_kg": 25.5,
  "status": "pending",
  "created_at": "2024-01-15T10:30:00.123456+00:00"
}
```

### 2. Get Shipment by Tracking Code

```bash
curl -X GET "http://localhost:8000/shipments/tracking/SHP-20240115-ABC12" \
  -H "X-API-Key: your-super-secret-api-key"
```

### 3. Update Shipment Status

```bash
curl -X PATCH "http://localhost:8000/shipments/1" \
  -H "X-API-Key: your-super-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_transit"
  }'
```

### 4. List All Shipments

```bash
curl -X GET "http://localhost:8000/shipments/?skip=0&limit=10" \
  -H "X-API-Key: your-super-secret-api-key"
```

## Database Schema

### Shipments Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| `tracking_code` | VARCHAR(50) | UNIQUE, NOT NULL, INDEXED | Auto-generated tracking code |
| `origin` | VARCHAR(255) | NOT NULL | Shipment origin |
| `destination` | VARCHAR(255) | NOT NULL | Shipment destination |
| `status` | ENUM | NOT NULL, DEFAULT='pending' | Current shipment status |
| `weight_kg` | FLOAT | NOT NULL | Weight in kilograms |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT=NOW() | Creation timestamp |

**Status Values:** `pending`, `in_transit`, `delivered`, `cancelled`

## Authentication

The API uses API Key authentication via the `X-API-Key` header.

- **Header:** `X-API-Key`
- **Default Key:** Check `.env` file
- **Invalid Key Response:** HTTP 401 Unauthorized

> ⚠️ **TODO:** Replace with JWT authentication in production. See [Production Setup](#production-setup).

## Production Setup

### Security Considerations

1. **JWT Authentication:** Replace API key auth with JWT tokens
   - Implement token generation and validation
   - Add token expiration and refresh mechanisms
   - Secure token storage on client side

2. **CORS Configuration:** Restrict to specific origins
   ```python
   # In app/main.py
   allow_origins=[
       "https://yourdomain.com",
       "https://app.yourdomain.com",
   ]
   ```

3. **Environment Variables:** Use secure secret management
   - Never commit `.env` files
   - Use environment variable management tools
   - Rotate secrets regularly

4. **Database:** Configure for production
   - Use connection pooling
   - Enable SSL/TLS for database connections
   - Regular backups

5. **API Rate Limiting:** Implement rate limiting
   - Prevent abuse and DoS attacks
   - Use `slowapi` library or similar

6. **Logging & Monitoring:** Set up comprehensive logging
   - Log all API requests
   - Monitor database performance
   - Set up alerts for errors

## Development

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations (Future)

For managing schema changes in production, consider using Alembic:

```bash
pip install alembic
alembic init migrations
```

## Troubleshooting

### Database Connection Error

```
Error: could not connect to server: Connection refused
```

**Solution:**
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env`
- Verify database credentials

### API Key Authentication Failed

```
HTTP 401: Invalid API key
```

**Solution:**
- Verify X-API-Key header is included in request
- Check API_KEY in `.env`
- Ensure header spelling is correct

### Port Already in Use

```
Address already in use
```

**Solution:**
```bash
# Change port
python -m uvicorn app.main:app --reload --port 8001
```

## License

MIT License

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## Support

For issues and questions, please open an issue in the repository.
