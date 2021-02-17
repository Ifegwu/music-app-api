release: python manage.py makemigration  --no-input
release: python manage.py migrate  --no-input

web: gunicorn music-app-api.app.app.wsgi