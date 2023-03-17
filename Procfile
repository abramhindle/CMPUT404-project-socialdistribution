release: python ./socialdistribution/manage.py migrate && python ./socialdistribution/manage.py collectstatic
web: cd socialdistribution && gunicorn socialdistribution.wsgi