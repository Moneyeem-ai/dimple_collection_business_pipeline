from .base import *
from decouple import config

import environ

env = environ.Env()
env.read_env(str(BASE_DIR / ".env-prod"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = [ "0.0.0.0", "pipeline.officedimple.co.in", "103.92.103.54"]
ALLOWED_HOST = ['*']

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRESS_NAME"),
        'USER': env("POSTGRESS_USER"),
        'PASSWORD': env("POSTGRESS_PASSWORD"),
        'HOST': env("POSTGRESS_HOST"),
        'PORT': env("POSTGRESS_PORT")
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = False

