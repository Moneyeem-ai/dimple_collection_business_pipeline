import os
import environ

from celery import Celery
from celery.signals import setup_logging

from config.settings.base import BASE_DIR


env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

app = Celery("apps")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)
