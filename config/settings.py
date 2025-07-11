import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True
# DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rooms',
    'api',
    'rest_framework',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки REST framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',  # Разрешить доступ всем пользователям
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ENV
CALDAV_URL = os.getenv("CALDAV_URL")
CALDAV_USERNAME = os.getenv("CALDAV_USERNAME")
CALDAV_PASSWORD = os.getenv("CALDAV_PASSWORD")

CALDAV_FIRST_FLOOR_PUBLIC = os.getenv("CALDAV_FIRST_FLOOR_PUBLIC")
CALDAV_SECOND_FLOOR_PUBLIC = os.getenv("CALDAV_SECOND_FLOOR_PUBLIC")
CALDAV_THIRD_FLOOR_PUBLIC = os.getenv("CALDAV_THIRD_FLOOR_PUBLIC")
CALDAV_CLASS_ROOM_PUBLIC = os.getenv("CALDAV_CLASS_ROOM_PUBLIC")

CALDAV_FIRST_FLOOR_URL = os.getenv("CALDAV_FIRST_FLOOR_URL")
CALDAV_FIRST_FLOOR_USERNAME = os.getenv("CALDAV_FIRST_FLOOR_USERNAME")
CALDAV_FIRST_FLOOR_PASSWORD = os.getenv("CALDAV_FIRST_FLOOR_PASSWORD")

CALDAV_THIRD_FLOOR_URL = os.getenv("CALDAV_THIRD_FLOOR_URL")
CALDAV_THIRD_FLOOR_USERNAME = os.getenv("CALDAV_THIRD_FLOOR_USERNAME")
CALDAV_THIRD_FLOOR_PASSWORD = os.getenv("CALDAV_THIRD_FLOOR_PASSWORD")

API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")

ROOM1 = os.getenv("ROOM1")
