release: cd backend && python manage.py migrate
web: gunicorn --pythonpath backend network.wsgi --log-file - && npm run start