```markdown
# Orthodontist Site

Full-stack website for an orthodontist with online appointment booking. 
It includes a Next.js frontend, Django + DRF backend, PostgreSQL,
and an Nginx gateway, all wired with Docker Compose and GitHub Actions CI/CD. 
reCAPTCHA v3 and CSRF are enabled end-to-end.

---

## Features

- Public pages: Services, Portfolio (Works), About.
- Appointment form: name, phone, preferred date, comment.
- Client & server validation:
    - Phone regex: `^(?:\+7|8)\d{10}$`
    - Preferred date cannot be in the past.
- reCAPTCHA v3 (action: `appointment`) on the frontend + server-side verification.
- CSRF protection (cookie + `X-CSRFToken` header).
- Django Admin to manage:
    - Appointments (statuses: `new`, `repeat`, `confirmed`, `done`, `canceled`)
    - Services, Works, About content.
- Health endpoints for monitoring.

---

## Tech Stack

- Frontend: Next.js (React), Framer Motion
- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Gateway: Nginx (reverse proxy; serves static/media)
- CI/CD: GitHub Actions → Docker Hub → SSH deploy
- Runtime: Docker / Docker Compose

---

## Repository Layout

```

backend/                     # Django + DRF project (orthodontist\_site)
frontend/                    # Next.js app
nginx/                       # Gateway config and Dockerfile
.github/workflows/ci.yml     # CI/CD pipeline
docker-compose.yml           # Orchestration

````

---

## API Overview

- `GET /api/services/` — list services  
- `GET /api/works/` — list portfolio items  
- `GET /api/about/` — get “About” page  
- `GET /api/csrf/` — sets CSRF cookie (`csrftoken`)  
- `POST /api/appointments/` — create appointment

**Create appointment — request body (JSON):**
```json
{
  "name": "Ivan",
  "phone": "+71234567890",
  "preferred_date": "2025-12-31",
  "message": "Optional comment",
  "recaptcha_token": "<token from grecaptcha.execute>"
}
````

**cURL example:**

```bash
# 1) Get CSRF cookie
curl -c cookies.txt https://<HOST>/api/csrf/

# 2) POST with CSRF header + reCAPTCHA token
curl -b cookies.txt \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $(grep csrftoken cookies.txt | awk '{print $7}')" \
  -d '{"name":"Ivan","phone":"+71234567890","preferred_date":"2025-12-31","message":"hi","recaptcha_token":"<token>"}' \
  https://<HOST>/api/appointments/
```

**Response codes:**

* `201 Created` — appointment saved (returns created object)
* `400 Bad Request` — validation errors or reCAPTCHA failed

---

## Frontend reCAPTCHA Flow

* Load script:

  ```
  https://www.google.com/recaptcha/api.js?render=<NEXT_PUBLIC_RECAPTCHA_SITE_KEY>
  ```
* Execute on submit:

  ```ts
  const token = await grecaptcha.execute(siteKey, { action: 'appointment' });
  ```
* Send `token` as `recaptcha_token` in POST body.

> Ensure your site domain is added in the reCAPTCHA console. The backend checks `action === "appointment"` and `score >= 0.5`.

---

## Quick Start (Docker)

1. Create a **`.env`** file in the repo root (see example below).
2. Start services:

   ```bash
   docker compose up -d
   ```
3. Create a Django superuser if needed:

   ```bash
   docker exec -it ortho_backend python manage.py createsuperuser
   ```
4. Admin panel: `https://<HOST>/admin/`

### Example `.env` (root)

```env
# PostgreSQL
POSTGRES_DB=orthodb
POSTGRES_USER=ortho_user
POSTGRES_PASSWORD=ortho_password
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=your.domain,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your.domain
CORS_ALLOWED_ORIGINS=https://your.domain
DJANGO_SETTINGS_MODULE=orthodontist_site.settings.docker

# reCAPTCHA (v3)
RECAPTCHA_SECRET=your_recaptcha_v3_secret
```

### Frontend build args

Provided at image build time (CI does this automatically):

* `NEXT_PUBLIC_API_URL=https://your.domain`
* `NEXT_PUBLIC_RECAPTCHA_SITE_KEY=your_recaptcha_v3_site_key`

---

## CI/CD

* **Selective builds:** Only services with changes are rebuilt (via `dorny/paths-filter`).
* **Tags:** Images are pushed with the commit SHA and also with a stable `:prod` tag.
* **Manual deploys:** You can use the “Run workflow” button to redeploy `:prod` images without rebuilding.
* **Deploy job:** Runs over SSH on the server:

    * Exports `TAG` (commit SHA or `prod`)
    * Runs `/srv/jml/deploy.sh` → `docker compose pull` + `up -d --remove-orphans` → prune old images.

---

## Useful Production Commands

Check that the backend sees the reCAPTCHA secret:

```bash
docker exec ortho_backend python -c "import os; from django.conf import settings; \
print('ENV secret?', bool(os.getenv('RECAPTCHA_SECRET'))); \
print('SETTINGS secret?', bool(getattr(settings,'RECAPTCHA_SECRET','')))"
```

Inspect effective Django `docker.py` settings inside the container:

```bash
docker exec ortho_backend sh -lc \
"python -c 'import importlib; m=importlib.import_module(\"orthodontist_site.settings.docker\"); print(open(m.__file__).read())'"
```

Tail backend logs (Gunicorn/Django):

```bash
docker logs -f ortho_backend
```

---

## reCAPTCHA v3 Troubleshooting

If you see `400 {"detail":"reCAPTCHA failed"}`:

1. Token missing on backend
   Logs may show: `reCAPTCHA: missing token or secret`

    * Ensure frontend sends `recaptcha_token`.
    * Confirm `RECAPTCHA_SECRET` is present in the container and in Django settings.

2. Wrong domain or site/secret keys

    * Add your domain to the reCAPTCHA admin console.
    * Verify you’re using v3 keys (site key on frontend, secret key on backend).

3. Action / score mismatch

    * The backend checks `result.action == "appointment"` and `score >= 0.5`.

4. Network issues to Google verify endpoint

    * Backend must reach `https://www.google.com/recaptcha/api/siteverify`.

---

## License

MIT — see [LICENSE](LICENSE).


