# ─── .github/scripts/smoke_backend.sh ───
#!/usr/bin/env bash
set -euo pipefail

image="$1"          # agasan/ortho_backend:SHA
secret="$2"         # RECAPTCHA_SECRET

docker run -d --name ortho_test \
  -e DJANGO_SETTINGS_MODULE=orthodontist_site.settings.docker \
  -e RECAPTCHA_SECRET="$secret" \
  -p 8000:8000 \
  "$image"

for i in $(seq 1 30); do
  docker logs ortho_test 2>&1 | grep -q "Starting gunicorn" && break
  sleep 1
done

docker exec ortho_test curl -sf http://localhost:8000/health/ >/dev/null
echo "✔ health-check passed"

docker rm -f ortho_test
