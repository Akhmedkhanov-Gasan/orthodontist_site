# Orthodontist Site

Full-stack website for an orthodontic clinic: public marketing pages, online appointment form, Django admin panel, media-backed content, Telegram bot, Docker deployment, and GitHub Actions CI/CD.

## Stack

- Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS, Framer Motion
- Backend: Django 5.1, Django REST Framework
- Database: PostgreSQL in Docker, SQLite for local Django settings
- Media/Admin: django-filer, easy-thumbnails, django-grappelli
- Bot: python-telegram-bot, Redis-backed runtime environment
- Gateway: Nginx reverse proxy
- CI/CD: GitHub Actions, Docker Hub, SSH deploy
- Runtime: Docker Compose

## Repository Layout

```text
backend/                 Django project and DRF API
frontend/                Next.js application
nginx/                   Nginx reverse proxy image and config
.github/workflows/       CI/CD pipeline
.github/scripts/         Helper scripts
media/                   Local media files, ignored in git
others/                  Local auxiliary files, ignored in git
docker-compose.yml       Local/prod service orchestration
.env.ci                  CI environment template
.env.frontend.example    Frontend environment example
```

## Application Features

- Public pages:
  - `/` - home page
  - `/services` - services
  - `/portfolio` - works / cases
  - `/about` - about page
  - `/about/team` - team page
  - `/appointment` - appointment form
- Dynamic content is managed through Django Admin.
- Appointment form uses:
  - client-side validation
  - server-side DRF validation
  - CSRF cookie and `X-CSRFToken`
  - Google reCAPTCHA v3 with action `appointment`
- Admin manages:
  - homepage content
  - about page content
  - team members
  - services
  - works / portfolio
  - appointments
  - patients
  - patient images
- Telegram bot can:
  - register a patient
  - accept a phone number
  - create an appointment request
  - notify an admin chat when configured
- Health endpoints are available for checks.

## Backend API

All API routes are served under `/api/`.

```text
GET  /api/home/           Homepage content
GET  /api/services/       Service list
GET  /api/works/          Portfolio work list
GET  /api/about/          About page with active team members
GET  /api/csrf/           Set CSRF cookie
GET  /api/ping/           Lightweight liveness check, returns pong
GET  /api/health/         Database health check
POST /api/appointments/   Create appointment
```

### Appointment Request

```json
{
  "name": "Ivan Ivanov",
  "phone": "+79991234567",
  "preferred_date": "2026-05-25",
  "message": "Optional comment",
  "recaptcha_token": "token-from-grecaptcha"
}
```

Validation rules:

- `name` is stripped, normalized, and cannot be empty.
- `phone` must match `+7XXXXXXXXXX` or `8XXXXXXXXXX`.
- `preferred_date` cannot be in the past.
- reCAPTCHA must pass unless `DISABLE_RECAPTCHA=1`.

## Frontend Runtime

The frontend expects these public variables:

```env
NEXT_PUBLIC_API_URL=https://your-domain.example
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=your_recaptcha_v3_site_key
```

`NEXT_PUBLIC_API_URL` is used for:

- loading page content from DRF
- loading media URLs
- requesting `/api/csrf/`
- submitting appointments

In Docker Compose these values are read from `.env.frontend`.

For local Next.js development, place equivalent values in `frontend/.env.local` or export them in the shell before running the dev server.

## Backend Environment

Production/Docker settings use `orthodontist_site.settings.docker`.

Required variables:

```env
POSTGRES_DB=orthodb
POSTGRES_USER=ortho_user
POSTGRES_PASSWORD=change-me
DB_HOST=db
DB_PORT=5432

SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=your-domain.example,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your-domain.example
CORS_ALLOWED_ORIGINS=https://your-domain.example

RECAPTCHA_SECRET=your_recaptcha_v3_secret

TELEGRAM_BOT_TOKEN=
TELEGRAM_ADMIN_CHAT_ID=
TELEGRAM_PROXY_URL=
REDIS_URL=redis://redis:6379/0
```

CI additionally uses:

```env
DISABLE_RECAPTCHA=1
DJANGO_SETTINGS_MODULE=orthodontist_site.settings.docker
```

## Docker Compose

Services:

```text
db        PostgreSQL 13.10
redis     Redis 7 Alpine
backend   Django + Gunicorn on port 8000 inside the network
frontend  Next.js on port 3000
gateway   Nginx on 127.0.0.1:8080
bot       Telegram bot using the backend image
```

Named volumes:

```text
pg_data   PostgreSQL data
static    Django collected static files
media     Uploaded media files
```

Start the full stack:

```bash
docker compose up -d --build
```

Apply migrations and collect static:

```bash
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py collectstatic --noinput
```

Create admin user:

```bash
docker compose run --rm backend python manage.py createsuperuser
```

Open:

```text
Frontend through gateway: http://127.0.0.1:8080/
Frontend direct:          http://localhost:3000/
Admin:                    http://127.0.0.1:8080/admin/
API:                      http://127.0.0.1:8080/api/
```

## Local Development

Backend with local settings:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate --settings=orthodontist_site.settings.local
python manage.py runserver --settings=orthodontist_site.settings.local
```

Frontend:

```bash
cd frontend
npm ci --legacy-peer-deps
npm run dev
```

Useful frontend checks:

```bash
npm run build
npx tsc --noEmit
```

Backend tests:

```bash
cd backend
pytest
```

Docker-based backend tests, matching CI more closely:

```bash
cp .env.ci .env
cp .env.frontend.example .env.frontend
docker compose build backend
docker compose up -d db redis
docker compose run --rm backend pytest
docker compose down -v
```

## Nginx Routing

The gateway listens on port `80` inside the container and is published as `127.0.0.1:8080` by Compose.

Routes:

```text
/admin/   -> backend:8000/admin/
/api/     -> backend:8000/api/
/media/   -> media volume
/static/  -> static volume
/         -> frontend:3000
```

## CI/CD

The pipeline is defined in `.github/workflows/deploy.yml`.

Triggers:

- push to `main`
- manual `workflow_dispatch`

Pipeline stages:

1. Preflight checkout and deployment target logging.
2. Backend tests:
   - copies `.env.ci` to `.env`
   - copies `.env.frontend.example` to `.env.frontend`
   - builds backend image
   - starts `db` and `redis`
   - runs `pytest` in Docker Compose
3. Frontend checks:
   - installs dependencies with `npm ci --legacy-peer-deps`
   - runs `npx tsc --noEmit`
   - runs production build with frontend secrets
4. Docker image builds:
   - backend image: `agasan/ortho_backend:<sha>` and `agasan/ortho_backend:prod`
   - frontend image: `agasan/ortho_frontend:<sha>` and `agasan/ortho_frontend:prod`
   - gateway image: `agasan/ortho_gateway:<sha>` and `agasan/ortho_gateway:prod`
5. Server deploy over SSH:
   - goes to `/home/gasan/orthodontist_site`
   - fetches `origin/main`
   - resets server repo to `origin/main`
   - pulls backend, frontend, and gateway images
   - runs Django migrations
   - runs `collectstatic`
   - restarts backend, frontend, gateway, and bot
   - checks gateway container status

Required GitHub secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
FRONTEND_API_URL
RECAPTCHA_SITE_KEY
SERVER_IP
SSH_USER
SSH_KEY
```

## Telegram Bot

The bot runs as a separate Compose service:

```text
bot -> agasan/ortho_backend:prod -> python manage.py runbot
```

Required for bot startup:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
```

Optional:

```env
TELEGRAM_ADMIN_CHAT_ID=admin_chat_id
TELEGRAM_PROXY_URL=socks_or_http_proxy
```

The bot uses polling and supports:

```text
/start
/register
/appointment
/contacts
/info
```

## Production Notes

- Uploaded media is stored in the shared `media` Docker volume and served by Nginx.
- Static files are collected into the shared `static` Docker volume and served by Nginx.
- reCAPTCHA v3 must be configured for the production domain.
- `CSRF_TRUSTED_ORIGINS` and `CORS_ALLOWED_ORIGINS` must include the real frontend origin.
- `DISABLE_RECAPTCHA=1` should only be used in CI or local testing.
- The workflow currently rebuilds all three deployable images on each `main` push.

## Useful Commands

Check running containers:

```bash
docker compose ps
```

Backend logs:

```bash
docker logs -f ortho_backend
```

Frontend logs:

```bash
docker logs -f ortho_frontend
```

Gateway logs:

```bash
docker logs -f ortho_nginx
```

Bot logs:

```bash
docker logs -f ortho_bot
```

Run migrations:

```bash
docker compose run --rm --no-deps backend python manage.py migrate
```

Collect static:

```bash
docker compose run --rm --no-deps backend python manage.py collectstatic --noinput
```

Check backend health through gateway:

```bash
curl http://127.0.0.1:8080/api/ping/
curl http://127.0.0.1:8080/api/health/
```

## License

No license file is currently included in the repository.
