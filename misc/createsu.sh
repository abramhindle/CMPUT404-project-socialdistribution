#!/bin/bash

# your heroku app name here
herokuappname=c404-w2021-t1-social-distribut

if [[ ! -n $(command -v heroku) ]]
then
  echo "You have to install heroku first!"
  exit 1
fi
# proxychains heroku login # only if you need to use proxy!
heroku login
# proxychains heroku run --app $herokuappname python manage.py createsuperuser # only if you need to use proxy!
heroku run --app $herokuappname python manage.py createsuperuser