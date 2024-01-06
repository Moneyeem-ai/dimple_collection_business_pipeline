import os

from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
settings.configure()

app = Celery('apps', backend='rpc://', broker='pyamqp://manas:1234@localhost:5672/')

app.config_from_object('django.conf:settings',namespace='CELERY')


@app.task
def add(x,y):
    return x+y
