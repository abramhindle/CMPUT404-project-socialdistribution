release: python manage.py migrate
web: gunicorn backend.wsgi --log-file -
web: node build/server.js
