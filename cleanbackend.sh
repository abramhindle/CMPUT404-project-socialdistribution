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

rm -rf ./backend
