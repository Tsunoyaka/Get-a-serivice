run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

restartdb:
	python3 manage.py makemigrations account
	python3 manage.py makemigrations statement
	python3 manage.py makemigrations service
	python3 manage.py migrate
	python3 manage.py createsuperuser