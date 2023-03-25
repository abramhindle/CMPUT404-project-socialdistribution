#!/bin/sh
# Start the backend
python3 social_net/manage.py migrate
python3 social_net/manage.py runserver