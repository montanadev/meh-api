.PHONY: run run-worker shell migrate makemigrations test test-coverage

run:
	poetry run ./manage.py runserver

run-worker:
	poetry run ./manage.py worker

shell:
	poetry run ./manage.py shell

migrate:
	poetry run ./manage.py migrate

makemigrations:
	poetry run ./manage.py makemigrations

collectstatic:
	poetry run ./manage.py collectstatic

test:
	poetry run ./manage.py test
