# Quick Start Guide

Get the Flowdesk backend API running in minutes!

## Option 1: Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed

### Steps

1. **Start PostgreSQL with Docker:**
   ```bash
   docker-compose up -d
   ```
   This starts:
   - PostgreSQL on port 5432
   - pgAdmin on http://localhost:5050 (admin/admin)

2. **Create Python Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment:**
   ```bash
   copy .env.example .env
   ```
   The default DATABASE_URL in `.env.example` is already configured for Docker.

5. **Initialize Database:**
   ```bash
   python init_db.py
   ```

6. **Run the API:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

7. **Access the API:**
   - API Docs: http://localhost:8000/docs
   - API Base: http://localhost:8000

---

## Option 2: Manual PostgreSQL Setup

### Prerequisites
- PostgreSQL installed and running
- Python 3.8+

### Steps

1. **Create Database:**
   ```bash
   createdb flowdesk
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   ```bash
   copy .env.example .env
   ```
   Update DATABASE_URL if your PostgreSQL credentials differ:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/flowdesk
   ```

5. **Initialize Database:**
   ```bash
   python init_db.py
   ```

6. **Start API:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

7. **Access API:**
   - API Docs: http://localhost:8000/docs

---

## Testing the API

### 1. Create a Shipment

Open Swagger UI at http://localhost:8000/docs and:

1. Click on "POST /shipments/"
2. Click "Try it out"
3. In the `X-API-Key` header, enter: `secret-api-key-change-in-production`
4. In the request body, enter:
   ```json
   {
     "origin": "New York",
     "destination": "Los Angeles",
     "weight_kg": 25.5,
     "status": "pending"
   }
   ```
5. Click "Execute"

You'll get back a shipment with an auto-generated tracking code:
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

### 2. Get All Shipments

1. Click on "GET /shipments/"
2. Click "Try it out"
3. Enter the API key: `secret-api-key-change-in-production`
4. Click "Execute"

### 3. Update Shipment Status

1. Click on "PATCH /shipments/{shipment_id}"
2. Enter `shipment_id`: `1`
3. Enter the API key
4. In the request body:
   ```json
   {
     "status": "in_transit"
   }
   ```
5. Click "Execute"

---

## Environment Variables

### Required
- `DATABASE_URL`: PostgreSQL connection string
- `API_KEY`: API key for authentication

### Optional
- `API_TITLE`: API documentation title
- `API_VERSION`: API version number

---

## Troubleshooting

### "Can't connect to database"
- Check PostgreSQL is running: `psql --version`
- For Docker: `docker-compose ps` should show postgres running
- Verify DATABASE_URL in `.env`

### "ModuleNotFoundError: No module named 'fastapi'"
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "Port 8000 already in use"
- Use a different port:
  ```bash
  python -m uvicorn app.main:app --reload --port 8001
  ```

### "401 Unauthorized"
- Ensure you're including `X-API-Key` header in requests
- Check API_KEY value in `.env`

---

## Next Steps

- Read [README.md](README.md) for full API documentation
- Check [app/routers/shipments.py](app/routers/shipments.py) for endpoint details
- See [PRODUCTION.md](PRODUCTION.md) for deployment guidelines (coming soon)

---

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f postgres

# Access PostgreSQL CLI
docker exec -it flowdesk-postgres psql -U postgres -d flowdesk

# Remove everything (including data)
docker-compose down -v
```

---

## API Key Header

All API requests require the `X-API-Key` header:

```bash
curl -X GET http://localhost:8000/shipments/ \
  -H "X-API-Key: secret-api-key-change-in-production"
```

Default key: `secret-api-key-change-in-production` (change in production!)

---

Happy shipping! 🚚
