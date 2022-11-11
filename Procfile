release: cd backend && python manage.py migrate && python manage.py loaddata prod_seed.json
web: gunicorn --pythonpath backend social_distribution.wsgi