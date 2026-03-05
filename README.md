# Health Records App

A headless FastAPI + SQLite backend with a vanilla JS/HTML/CSS frontend, structured for production.

---

## Project Structure

```
health-records/
├── backend/
│   ├── main.py                  # Entry point (uvicorn target)
│   ├── requirements.txt
│   ├── records.db               # SQLite DB (auto-created on startup)
│   └── app/
│       ├── __init__.py          # App factory (create_app)
│       ├── config.py            # Centralised settings / env vars
│       ├── db/
│       │   ├── __init__.py
│       │   └── database.py      # Connection manager, init_db
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py       # Pydantic request / response models
│       └── routers/
│           ├── __init__.py
│           └── records.py       # CRUD route handlers
└── frontend/
    ├── index.html               # Markup only — no inline styles or scripts
    ├── css/
    │   └── styles.css           # All styles (design tokens, layout, components)
    └── js/
        ├── api.js               # HTTP layer — all fetch calls isolated here
        ├── ui.js                # DOM layer — all rendering isolated here
        └── app.js               # Entry point — wires api.js + ui.js together
```

---

## Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

| URL | Description |
|-----|-------------|
| `http://localhost:8000/docs`  | Interactive Swagger UI |
| `http://localhost:8000/redoc` | ReDoc documentation |
| `http://localhost:8000/health`| Health check endpoint |

---

## Frontend Setup

No build step required.

```bash
# Serve with Python (recommended — avoids file:// CORS edge cases)
cd frontend
python -m http.server 3000
# Visit http://localhost:3000
```

---

## API Reference

| Method | Endpoint           | Description       |
|--------|--------------------|-------------------|
| GET    | /health            | API health check  |
| GET    | /records/          | List all records  |
| GET    | /records/{id}      | Get one record    |
| POST   | /records/          | Create a record   |
| PUT    | /records/{id}      | Update a record   |
| DELETE | /records/{id}      | Delete a record   |

### POST /records/ — request body

```json
{
  "firstname": "Jane",
  "lastname":  "Smith",
  "age":       30,
  "sex":       "female",
  "health":    "athletic"
}
```

Valid `health` values: `athletic` · `good` · `average` · `poor`
Valid `sex` values: `male` · `female` · `other`

---

## Environment Variables

| Variable       | Default                     | Description                    |
|----------------|-----------------------------|--------------------------------|
| `DEBUG`        | `false`                     | Enable debug mode              |
| `DB_PATH`      | `backend/records.db`        | Path to SQLite database file   |
| `CORS_ORIGINS` | `*`                         | Comma-separated allowed origins|
