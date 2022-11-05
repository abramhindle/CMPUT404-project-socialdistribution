release: cd backend && python manage.py migrate
web: gunicorn --pythonpath backend social_distribution.wsgi