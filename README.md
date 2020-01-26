# CMPUT404-Group Project

## Overview

### Technologies
* Django
* ReactJS
* Heroku

### Structure

```
Project/
|-- backend  # Django API server
|-- src      # ReactJS Frontend SPA
|-- public   # React Public Folder
|-- Profile  # Heroku config
|-- manage.py # Django manage.py
|-- package.json # Node packages
|-- requirement.txt # Python packages
```

## Setup & Run

First, clone the repo
```
    git clone https://github.com/CMPUT404W20/CMPUT404-project-socialdistribution.git
```
### Setup Virtualenv
Make sure you are using python>=3 and pip3
```
cd CMPUT404-project-socialdistribution/

# Install virtualenv
python3 -m pip install --user virtualenv

python3 -m venv env

# activate the virtualenv
source env/bin/activate
```

### Install Backend dependencies
```
# Install all pip packages
pip3 install -r requirements.txt

# Verify packages are successfully installed
pip3 freeze

```
### Install Frontend dependencies
Make sure you have node and yarn installed, if not, refers to :
- [**Node Install Page**](https://nodejs.org/en/download/)
- [**Yarn Install Page**](https://legacy.yarnpkg.com/lang/en/docs/install/)
```
    yarn install
```

### Add secrets
```
touch .env
echo 'DATABASE_URL=sqlite:///db.sqlite3' > .env
```
Currently, we only have database information in secret file
Information on databases will be explained later in this README

### Run the Project

For development, we need to run both frontend and backend servers
```
yarn start
source env/bin/activate
python manage.py migrate
python manage.py runserver
```

If you are only working on backend, and therefore don't need to worry about the frontend, to make your life easier, you can do

```
yarn build
source env/bin/activate
python manage.py migrate
python manage.py runserver
```

## Deployment
Make sure you have Heroku CLI installed.
Read [**this**](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) if you haven't.
And read[**this**](https://devcenter.heroku.com/articles/heroku-cli#getting-started) to step up

Both Frontend SPA and Backend API are hosted on Heroku.
To deploy changes on server
```
git push heroku master
```
after you have commit your changes

## Databases Information
Our production Postgres database is hosted on Heroku.
For local development, we will use `sqlite` in order to keep our production database clean, and if you want to add an entry to our remote database,You will need to do it through Heroku CLI
For example, add a superuser, you can do
```
heroku run python manage.py createsuperuser
```

## Troubleshooting
* Check your dependencies and environment
* Reach out to Yuxuan(Xavier)
* [**Or ask your best friend**](https://www.google.ca/)