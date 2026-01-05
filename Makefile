migrations:
	cd src && python3 manage.py makemigrations

migrate:
	cd src && python3 manage.py migrate

run:
	cd src && python3 manage.py runserver