web: gunicorn social_dist.wsgi --log-file -
release: python manage.py makemigrations --merge
release: python manage.py migrate