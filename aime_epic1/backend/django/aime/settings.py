import os
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------
# Paths + .env (works whether you run via Docker or locally)
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # .../backend/django
# Try common locations; later calls don't override earlier values
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")           # .../backend/.env  (your usual spot)
load_dotenv(BASE_DIR.parent.parent / ".env")    # repo root .env (fallback)

def env_bool(name, default=False):
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")

# -------------------------------------------------
# Core
# -------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-not-secure")
DEBUG = env_bool("DJANGO_DEBUG", default=env_bool("DEBUG", default=True))
ALLOWED_HOSTS = [h for h in os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",") if h]

# Optional, useful when serving via a real domain / reverse proxy
CSRF_TRUSTED_ORIGINS = [o for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o]

LANGUAGE_CODE = "ms"
TIME_ZONE = "Asia/Kuala_Lumpur"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Apps & middleware
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # enable static serving
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "aime.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "aime.wsgi.application"

# -------------------------------------------------
# Database (MySQL) – uses your env names
# -------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB", "aime"),
        "USER": os.getenv("MYSQL_USER", "aimeuser"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "aimesecret"),
        "HOST": os.getenv("MYSQL_HOST", "db"),   # 'db' inside Docker network
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TZ", default="UTC")
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Static files (WhiteNoise)
# -------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------
# FastAPI service location (Django -> FastAPI proxy in views)
# -------------------------------------------------
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8001"))
FASTAPI_INTERNAL_URL = os.getenv("FASTAPI_INTERNAL_URL", f"http://fastapi:{FASTAPI_PORT}")

# -------------------------------------------------
# Friendly Admin branding (uncomment if you want it active)
# -------------------------------------------------
# from django.contrib import admin
# admin.site.site_header = "AIME Admin"
# admin.site.site_title = "AIME Admin"
# admin.site.index_title = "Pengurusan AIME"
