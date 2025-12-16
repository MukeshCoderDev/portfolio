# Django Contact Backend

Production-ready contact form backend with async email processing.

## Quick Start

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Run Celery Worker (requires Redis)
```bash
celery -A config worker -l info
```

## API Endpoints

- `POST /api/contact/` - Submit contact form (public)
- `GET /api/admin/contacts/` - List messages (auth required)
- `GET /api/admin/contacts/{id}/` - Get message detail
- `PATCH /api/admin/contacts/{id}/` - Update status
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/health/` - Health check
