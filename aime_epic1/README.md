# AIME — EPIC 1 Starter (Django + FastAPI + MySQL + phpMyAdmin)

This starter sets up:
- Django (admin + chat UI) on http://localhost:8000
- FastAPI (future AI endpoints) on http://localhost:8001
- MySQL 8 with phpMyAdmin on http://localhost:8080
- Python 3.10+

## Quick start with Docker (recommended)
1) Install Docker Desktop.
2) Copy `.env.example` to `.env` and adjust secrets if needed.
3) Build & run:
   ```bash
   docker compose up --build
   ```
4) Open phpMyAdmin: http://localhost:8080
   - Server: `db` (already configured)
   - Username: `aimeuser`
   - Password: `aimesecret`
   Create DB if not created automatically: `aime`.
5) In another terminal, inside `backend/django`:
   ```bash
   docker compose exec django python manage.py migrate
   docker compose exec django python manage.py createsuperuser
   ```
6) Visit Django: http://localhost:8000 and Admin: http://localhost:8000/admin

## Manual local setup (no Docker)
1) Ensure MySQL is running and create a database `aime` and user/password.
2) Python 3.10+:
   ```bash
   cd backend/django
   python -m venv .venv
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   copy ../../.env.example ../../.env  # or manually create .env at project root
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
   Update `MYSQL_*` values in `.env` if needed.

## Where to put your premium Bootstrap template
- Copy your template assets (CSS/JS/images) into `backend/django/static/` and reference them in `templates/base.html`.
- Replace the CDN Bootstrap link with your template's CSS.
- Adjust classes in `templates/chat/chat.html` as desired.

## Django admin prepared for all EPICs
- KnowledgeBaseEntry model for FAQs/soalan.
- ConversationMessage model for logging chats.
- Admin branding set to "AIME Admin".

## FastAPI app (future EPIC 2+)
- A simple `/health` endpoint is included.
- You can add ML/LLM routes later (classification, password reset orchestration, etc).

## Security notes
- Change all default passwords/secrets in `.env`.
- In production, set `DEBUG=0` and configure ALLOWED_HOSTS properly.
