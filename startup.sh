#!/bin/sh

python ./manage.py migrate

# https://stackoverflow.com/questions/6244382/how-to-automate-createsuperuser-on-django
# By Tk421 on Sep 29, 2014 at 1:08
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell

python ./manage.py runserver 0.0.0.0:8000
