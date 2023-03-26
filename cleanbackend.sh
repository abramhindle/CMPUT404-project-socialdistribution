#!/bin/bash

rm -rf ./frontend
rm -rf ./likelikedver2
rm -rf ./testcase
rm -rf ./docker-compose.yml
rm -rf ./heroku.yml
rm -rf ./project.org
rm -rf ./backend/social_net/entrypoint.sh
rm -rf ./backend/social_net/Dockerfile
rm -rf ./backend/social_net/db.sqlite3

mv -iv ./backend/* ./backend/..

mkdir ./temp
mv -fv ./social_net/* ./temp

rm -rf ./backend
rm -rf ./social_net

mv -fv ./temp/* .
rm -rf ./temp
