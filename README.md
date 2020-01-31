# CMPUT404-Group Project
[![Build Status](https://travis-ci.com/CMPUT404W20/CMPUT404-project-socialdistribution.svg?branch=master)](https://travis-ci.com/CMPUT404W20/CMPUT404-project-socialdistribution)
## Overview

### Technologies
* Django
* ReactJS
* Heroku
* PostgreSQL

### Structure

```
Project/
|-- backend  # Django API server
|-- src      # ReactJS Frontend SPA
|-- public   # React Public Folder
|-- Procfile  # Heroku config
|-- manage.py # Django manage.py
|-- package.json # Node packages
|-- requirements.txt # Python packages
```

## Setup & Run

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
# Install PostgreSQL
brew install postgresql

# Install all python packages
pip3 install -r requirements.txt

# Verify packages are successfully installed
pip3 freeze
```
### Install Frontend dependencies
Make sure you have node and yarn installed, if not, refer to:
- [**Node Install Page**](https://nodejs.org/en/download/)
- [**Yarn Install Page**](https://legacy.yarnpkg.com/lang/en/docs/install/)
```
yarn install
yarn add react-scripts
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

### Run the Test

For running frontend tests, simply run
```
yarn test
```
For running backend tests, run
```
py.test backend
```
**It is `py.test` not pytest** <br>
After executing, it will generate a coverage report inside `htmlcov/` folder

### Install ESLint 
Please install the ESLint package for your IDE or Text Editor to help us maintain consistent and clean code. To make sure it is working, try using single quotes instead of double quotes - it should complain with single quotes. 
