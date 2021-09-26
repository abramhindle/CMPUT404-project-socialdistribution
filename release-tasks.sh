#!/bin/sh
# https://devcenter.heroku.com/articles/release-phase#specifying-release-phase-tasks
python manage.py migrate
python manage.py createsuperuser --noinput
