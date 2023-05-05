#!/bin/sh
cd /usr/bin/meh-api/
export PATH="/home/meh/.local/bin:$PATH"
poetry run python3 manage.py makemigrations
poetry run python3 manage.py migrate
poetry install
poetry run python3 manage.py runserver 0.0.0.0:80
