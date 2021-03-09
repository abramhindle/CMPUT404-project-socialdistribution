#!/bin/bash

# your heroku app name here
herokuappname=social-distribution-t1

# assume you alreay run predeploy.sh
if [[ ! -d "DeployMe" ]]
then
  echo "You need to run predeploy.sh first!"
  exit 1
fi
if [[ ! -n $(command -v heroku) ]]
then
  echo "You have to install heroku first!"
  exit 1
fi
heroku login
cd DeployMe
heroku git:remote -a $herokuappname
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
heroku addons:create heroku-postgresql:hobby-dev
git push heroku master