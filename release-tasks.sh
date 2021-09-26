#!/bin/sh
# https://devcenter.heroku.com/articles/release-phase#specifying-release-phase-tasks
python manage.py migrate

# create DJANGO_SUPERUSER_USERNAME if it doesn't exist
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model
import os

DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')

User = get_user_model()  # get the currently active user model,

User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists() or \
    User.objects.create_superuser(DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD)
EOF

