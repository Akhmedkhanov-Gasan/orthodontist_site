#!/usr/bin/env bash
set -euo pipefail

IMAGE="$1"          # registry/ortho_backend:tag
SECRET="$2"         # RECAPTCHA_SECRET

echo "▶️  Smoke-test $IMAGE"

docker run -d --name ortho_test \
  -e DJANGO_SETTINGS_MODULE=orthodontist_site.settings.docker \
  -e RECAPTCHA_SECRET="$SECRET" \
  -e ALLOWED_HOSTS=localhost \
  -p 8000:8000 "$IMAGE"

ATTEMPTS=30
for i in $(seq 1 $ATTEMPTS); do
  if curl -sf http://localhost:8000/api/ping/ >/dev/null; then
    echo "✅ backend is healthy (ping)"
    docker rm -f ortho_test
    exit 0
  fi
  sleep 2
done

echo "❌ health-check failed"
docker logs ortho_test || true
docker rm -f ortho_test
exit 1
