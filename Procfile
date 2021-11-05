release: cd backend && python manage.py migrate
web: npm run start
server: gunicorn --pythonpath backend network.wsgi --log-file -