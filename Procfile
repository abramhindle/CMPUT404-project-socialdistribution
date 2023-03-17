release: python ./socialdistribution/manage.py migrate
api: cd socialdistribution && gunicorn socialdistribution.wsgi
web: cd frontend && npm install && npm start