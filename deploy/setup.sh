#!/usr/bin/env bash

set -env
# TODO: Set to URL of git repo.

PROJECT_GET_URL='https://github.com/Ifegwu/music-app-api.git'

PROJECT_BASE_PATH='/usr/local/apps/music-app-api'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev postgresql python-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GET_URL $PROJECT_BASE_PATH

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/ docker-compose run app pipenv install gunicorn==19.9.0

# Run migration and collect static file
# $PROJECT_BASE_PATH/env/bin/ docker-compose run app sh -c "python manage.py migrate"
# $PROJECT_BASE_PATH/env/bin/ docker-compose run app sh -c "python manage.py collectstatic --no-input"

# Configure supervisor
cp $PROJECT_GET_URL/deploy/supervisor_music_api.conf /etc/supervisor/conf.d/music_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart music_api

# Configure nginx
cp $PROJECT_GET_URL/deploy/nginx_music_api.conf /etc/nginx/sites-available/music_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/music_api.conf /etc/nginx/sites-enabled/music_api.conf
systemctl restart nginx.service

echo "DONE! :)"