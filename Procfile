web: gunicorn 'config.wsgi' --log-file -
worker: celery -A config worker -E --concurrency=4 -l info