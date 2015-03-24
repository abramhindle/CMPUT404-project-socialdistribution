#!/bin/bash

# Run this to remove all previous migrations and redo the migrations

find -type d -name migrations -exec rm -rf {} \;

rm db.sqlite3

./manage.py migrate

./manage.py makemigrations author

./manage.py makemigrations comment

./manage.py makemigrations images

./manage.py makemigrations post

./manage.py makemigrations node

./manage.py migrate