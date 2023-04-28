#!/bin/sh
export PATH="/home/meh/.local/bin:$PATH"
poetry install
poetry run python3 manage.py runserver 0.0.0.0:80
