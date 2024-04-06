import os
import environ
from celery import Celery

from config.settings.base import BASE_DIR


env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

app = Celery("apps")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
