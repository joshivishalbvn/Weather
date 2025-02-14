from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

app = Celery('weather')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'get_wether_data': {
        'task': 'app_modules.weather_app.tasks.get_weather_data',
        'schedule': timedelta(minutes=30),
    },
}

# to start celery worker for this project
# celery -A weather worker --loglevel=info

# celery -A weather beat --loglevel=info


# reset the Celery worker connections:
# celery -A weather control reset