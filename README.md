# CMPUT404-project-socialdistribution

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

CMPUT404F21L802 Members:

    Ayabdall
    Matthew-Mullen
    Ohi-Ahimie
    Patrisha-de-Boon
    wowikc

# Contributing

Send a pull request and be sure to update this file with your name.

# Contributors / Licensing

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Project Team:

    Abdelrahman Abdalla
    Matthew Mullen
    Ohiwere Ahimie
    Patrisha de Boon
    Uladzimir Bondarau

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma
    Nhan Nguyen 

# Initializing Repo

Use a terminal in the class VM to navigate to a folder you wish to clone this repo into, then run the following commands to clone the repo and navigate into the directory:

```
git clone https://github.com/cmput404F21/CMPUT404-project-socialdistribution.git 
cd CMPUT404-project-socialdistribution
```

Next, create a virtual environment and install project requirements as follows:

```
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt # install requirements
```

# Creating a database

Configure local PostgreSQL DB for running the project:

```
source venv/bin/activate
sudo apt install libpq-dev postgresql                           # install postgres and its requirements
sudo -u postgres psql                                           # open Posgress console
#If you get an error here, try running $```sudo systemctl restart postgresql.service``` to restart the Postgres server
# In the Posgress console
postgres=#    CREATE DATABASE socialdistribution_db;            # Credentials as in settings.py
postgres=#    CREATE USER admin WITH PASSWORD 'admin';          # create user for DB use
postgres=#    ALTER ROLE admin SET client_encoding TO 'utf8';   # Set Postgress encoding
postgres=#    ALTER ROLE admin SET default_transaction_isolation TO 'read committed'; # Set transaction
postgres=#    GRANT ALL PRIVILEGES ON DATABASE socialdistribution_db TO admin; # Allow user access to DB
postgres=# ALTER USER admin CREATEDB; 
# Allows automated tests to create dbs
postgres=#    \q # to exit
```

# Reset db
```
# Remove migration files
# Make sure your vitrual environment is above socialdistribution_root, otherwise the following command will break django. If that happens, simply delete and recreate venv.
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
# Reset db
sudo -u postgres psql   
postgres=#      DROP database socialdistribution_db;
# pgAdmin needs to be closed, as it will prevent the drop
postgres=#      CREATE DATABASE socialdistribution_db;
postgres=#      GRANT ALL PRIVILEGES ON DATABASE socialdistribution_db TO admin;
postgres=#    \q # to exit
# Rerun migrations
```

# Running The Server

Now switch into the root folder ```cd socialdistribution_root```. Most django related commands will be run from this folder.

Run the following command from the _root_:

- Make migrations `python manage.py makemigrations`
- Migrate database `python manage.py migrate`
- Start the server `python manage.py runserver`
- To run tests `python manage.py test`


This will run the server and show you where the development server is being hosted, usually  http://127.0.0.1:8000/.

You can nagivate to this url from your web browser to see the home page.

# Authentication

To add the first super user (to allow logging in to the admin page) run the following command from the root and add your user information. 

```
python manage.py createsuperuser
```

To add additional users (admin or otherwise) to the server, log in to the admin page at http://127.0.0.1:8000/admin using your superuser credentials. Here you should be able to add a "user" object. In the future there will likely be a sign in page to allow users to (optionally request) sign in themselves.

Authentication was initilly based on the following tutorial
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication

# Django Structure

This project was partly created using the following guide for file structure and organization: 
https://djangobook.com/mdj2-django-structure/

Apps are also created in an apps folder to more clearly differentiate them from the primary site app 
and to keep the root folder a bit cleaner.

To create a new app (for example, one called 'appname') first create a new directory in the apps directory called appname. Then run the following command from the root folder

```
python manage.py startapp appname ./apps/appname
```

Next, add app.appname to INSTALLED_APPS in settings.py. 

Then, in the apps.py file of your new apps/appname directory, change the name inside the AppnameConfig class to 'apps.appname' instead of the default 'appname' it may have autogenerated.

# Sources

Sources that were referenced during the making of this project are listed in the relevent files and sections as well as below:

https://learndjango.com/tutorials/django-signup-tutorial
https://djangobook.com/mdj2-django-structure/
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication
https://www.django-rest-framework.org/tutorial/1-serialization/
