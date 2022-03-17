from pathlib import Path
from urllib.parse import urlparse
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1fon4d1f)xj3upklzud_xkf#lfke74okyw=*j6kbo$26^f0^_v'

# SECURITY WARNING: don't run with debug turned on in production!!
DEBUG = True

DOMAIN = str(os.environ.get("DOMAIN", default="http://127.0.0.1:8000"))
#DOMAIN = "http://project-socialdistribution.herokuapp.com"

ALLOWED_HOSTS = [urlparse(DOMAIN).netloc.split(":")[0]] + ["127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'notifications.apps.NotificationsConfig',
    'comment.apps.CommentConfig',
    'inbox.apps.InboxConfig',
    'authors.apps.AuthorsConfig',
    'posts.apps.PostsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Social Distribution API',
    'DESCRIPTION': 'The API For Social Distribution',
    'VERSION': '3.0.0',
    "swagger": "2.0"
}

CORS_ORIGIN_WHITELIST = [
    'http://project-socialdistribution.herokuapp.com',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "build")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

"""
db_from_env = dj_database_url.config()
DATABASES = {'default': dict()}
DATABASES['default'].update(db_from_env)
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'social_distribution',
        'USER': 'postgres',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '5433',
        'ATOMIC_REQUESTS': True
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    # Tell Django where to look for React's static files (css, js)
    os.path.join(BASE_DIR, "build/static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'