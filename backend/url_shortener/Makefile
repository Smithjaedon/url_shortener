run:
	python manage.py runserver

mm:
	python manage.py makemigrations
	python manage.py migrate

worker:
	celery -A url_shortener worker --loglevel=info

beat:
	celery -A url_shortener beat --loglevel=info

flower:
	celery -A url_shortener flower