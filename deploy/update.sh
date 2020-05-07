#!/usr/bin/env bash

set -c

PROJECT_BASE_PATH='/usr/local/apps/music-app-api'

git pull 
$PROJECT_BASE_PATH/ docker-compose run app sh -c "python manage.py migrate"
$PROJECT_BASE_PATH/ docker-compose run app sh -c "python manage.py collectstatic --no-input"
supervisorctl restart music_api

echo "DONE! :)"