#!/usr/bin/bash

echo start
date
git pull
poetry run python manage.py makemigrations
poetry run python manage.py migrate
echo end
date
