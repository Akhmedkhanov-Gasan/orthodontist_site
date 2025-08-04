# orthodontist_site/settings/local.py
from .base import *
from dotenv import load_dotenv, find_dotenv

PROJECT_ROOT = BASE_DIR.parent

load_dotenv(find_dotenv())
RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET", "dummy-secret")

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT / 'db.sqlite3',
    }
}


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
