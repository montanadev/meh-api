#!/bin/sh
cd /usr/bin/meh-api/meh-api/
git -C /usr/bin/meh-api/meh-api pull
/home/meh/.local/bin/poetry install -p /usr/bin/meh-api/meh-api/
/home/meh/.local/bin/poetry run python3 /usr/bin/meh-api/meh-api/manage.py makemigrations
/home/meh/.local/bin/poetry run python3 /usr/bin/meh-api/meh-api/manage.py migrate
/home/meh/.local/bin/poetry run python3 /usr/bin/meh-api/meh-api/manage.py runserver 0.0.0.0:80
