#!/bin/bash

# your heroku app name here
herokuappname=social-distribution-t1v2
# make sure you are using python3
pythonexecutable=python3

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
# proxychains heroku login # only if you need to use proxy!
heroku login
reactappconfigbase64=$(python3 env.py)
cd DeployMe
heroku git:remote -a $herokuappname
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
heroku config:set REACT_APP_CONFIGBASE64=$reactappconfigbase64
heroku addons:create heroku-postgresql:hobby-dev
git push heroku master