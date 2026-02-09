# lawyer_website/settings.py (минимальная версия)
import os
from pathlib import Path
import socket
from django.core.mail.utils import DNS_NAME


bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-key-12345-change-in-production'

DEBUG = True

# Разрешенные хосты (обязательно при DEBUG=False)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'saintptavo.com',    # Раскомментируйте для продакшена
    'lawyer-site.up.railway.app',
    '.railway.app',
    'https://gutorov777.pythonanywhere.com/',
    '0.0.0.0',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ↓↓↓ ДОБАВЬТЕ ЭТУ СТРОКУ ↓↓↓
    'lawyer_site',  # ← Ваше приложение
]

RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lawyer_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'lawyer_website.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6}
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mspelmen5@gmail.com'  # ваш Gmail
EMAIL_HOST_PASSWORD = 'vyxx xmfs tadr ftus'  # НЕ основной пароль!
DEFAULT_FROM_EMAIL = 'mspelmen5@gmail.com'
SERVER_EMAIL = 'mspelmen5@gmail.com'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки для загрузки медиафайлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = BASE_DIR / 'staticfiles'  # ← ДОБАВЬТЕ ЭТУ СТРОКУ