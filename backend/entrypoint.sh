#!/usr/bin/env sh
set -e
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver --noreload 0.0.0.0:8080