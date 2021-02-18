#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn music-app-api.app.app.wsgi -b 0.0.0.0:8000
# uwsgi --socket :8000 --master --enable-threads --module app.wsgi --chmod-socket=666