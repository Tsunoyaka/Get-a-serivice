run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

restartdb:
	dropdb silk_db
	createdb silk_db
	python3 manage.py makemigrations account
	python3 manage.py makemigrations silkAPI
	python3 manage.py migrate
	python3 manage.py createsuperuser