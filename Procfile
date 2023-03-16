release: python ./socialdistribution/manage.py migrate && cd frontend && npm run build
web: cd socialdistribution && gunicorn socialdistribution.wsgi
