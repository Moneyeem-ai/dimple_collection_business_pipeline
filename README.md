# Project Management

## Setup

- Create virtual environment using

- Activate the envirnoment

- Install local and base requeriements using

```
pip install -r requirements/base.txt
```

```
pip install -r requirements/local.txt
```

- Run migrations

```
python manage.py makemigrations
```

```
python manage.py migrate --run-syncdb
```

- Start the server
```
python manage.py runserver
```

## Getting mock data
- python manage.py create_users
- python manage.py create_roles
- python manage.py create_teams
- python manage.py create_projects
- python manage.py create_tasks
- python manage.py create_budgets

## Getting app password 
- Go To 'Manage Your Google Account' 
- Go to security tab 
- Then you will find a section 'How you sign in to Google'
- If 2-factor authentication is off, turn it on
- Then click on 2-Steps Verification and scroll to bottom 
- There you will find 'App Passwords'
- click on that and add an app password
- There in select app, you have to select Mail and in select device choice your device
- Once you generate a password, you can create a .env file in project's root directory

```
EMAIL_HOST_USER="YOUR_GMAIL_ID"
EMAIL_HOST_PASSWORD="GENERATED_APP_PASSWORD"
```

## Getting up redis for celery queue
- https://redis.io/docs/getting-started/installation/install-redis-on-windows/

## Running celery

celery -A config worker -E --concurrency=4 -l info

## References 
- https://appseed.us/
- https://github.com/cookiecutter/cookiecutter
