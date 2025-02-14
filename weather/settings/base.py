import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR


SECRET_KEY =  os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRDPARTY_APPS = [
    "daphne",
    "django_celery_beat",
    "django_celery_results",
    "django_select2",
    # "sslserver",
]

LOCAL_APPS = [
    "app_modules.weather_app",
]

INSTALLED_APPS = THIRDPARTY_APPS + LOCAL_APPS + DJANGO_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'weather.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [str(APPS_DIR / "templates")],
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

# WSGI_APPLICATION = 'weather.wsgi.application'
ASGI_APPLICATION = "weather.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    },
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME":  os.environ.get("DATABASE_NAME"),
#         "USER":  os.environ.get("DATABASE_USER"),
#         "PASSWORD":  os.environ.get("DATABASE_PASSWORD"),
#         "HOST":  os.environ.get("DATABASE_HOST"),
#         "PORT":  os.environ.get("DATABASE_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'weather'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': 'db',  
        'PORT': '5432',
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

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(APPS_DIR, "static")
STATICFILES_DIRS = [os.path.join(APPS_DIR, "static_files")] 

MEDIA_ROOT = os.path.join(APPS_DIR, "media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SUPER_USER = {
    "ADMIN_EMAIL": os.environ.get("ADMIN_EMAIL"),
    "ADMIN_USERNAME": os.environ.get("ADMIN_USERNAME"),
    "ADMIN_PASSWORD": os.environ.get("ADMIN_PASSWORD"),
}


# <-----------Celery----------->
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TIMEZONE = "Asia/Kolkata"
DJANGO_CELERY_BEAT_TZ_AWARE=False
# <-----------Celery----------->

# <-------------------------------- Select 2 ---------------------------------->
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': 'redis://redis:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
         'LOCATION': 'redis://redis:6379/2',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SELECT2_CACHE_BACKEND = 'default'
# <-------------------------------- Select 2 ---------------------------------->

OPEN_WEATHER_MAP_API_KEY = "4ab7025243672571567735d9bc0232d5"
GEO_APIFY_API_KEY = "b98d2839d16440749d9ce0dba844b317"

ALLOWED_HOSTS = ['*']