CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

Contributing
============

CMPUT 404 W23 H01 Members:
    Jeff
    Ferdous
    Curtis
    Zhengdao
    Victor

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Project Team 24:
    Jeff
    Ferdous
    Curtis
    Zhengdao
    Victor

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

# Initializing The Repo

Use a terminal to navigate to a folder you wish to clone this repo into, then run the following commands to clone the repo and navigate into the directory:

```
git clone https://github.com/yuchieh8968/CMPUT404-project-socialdistribution.git
cd CMPUT404-project-socialdistribution
```

Next, create a virtual environment and install project requirements as follows:

```
virtualenv venv --python=python3
source venv/bin/activate            # On Windows venv\Scripts\Activate
pip install -r requirements.txt
```

# Running The Server
Run the following command from the root folder ```CMPUT404-project-socialdistribution```:

- To collect static files `python manage.py collectstatic`
- To make migrations `python manage.py makemigrations`
- To migrate database `python manage.py migrate`
- To start the server `python manage.py runserver`

This will run the server and it will tell you where the development server is being hosted, usually http://127.0.0.1:8000/.
You can nagivate to this url from your web browser to see the home page.

- To run tests `python manage.py test`

# Creating a Database

**For Windows** first install PostgreSQL via https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

Follow this guide for installation and how to get to the Postgres console:
https://medium.com/@9cv9official/creating-a-django-web-application-with-a-postgresql-database-on-windows-c1eea38fe294

In the **psql** shell, accept the default for the **Server**, **Database**, **Port**, and **Username** fields by pressing Enter.
However, at the **Password** field, you must enter the password that you chose during the Installation Setup Wizard.

Next, follow the steps below (after you see the warning message and the line ```postgres=#```):

```
 postgres=# CREATE DATABASE social_distribution_db with ENCODING 'UTF-8';
 postgres=# CREATE USER admin WITH ENCRYPTED PASSWORD 'password';
 postgres=# GRANT postgres TO admin;
 postgres=# GRANT ALL PRIVILEGES ON DATABASE social_distribution_db to admin;
```

**For Linux** following this guide: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04

To configure your local PostgreSQL DB for the project, enter the following steps:

```
source venv/bin/activate
sudo apt install libpq-dev postgresql                           # Install Postgres
sudo -u postgres psql                                           # Open the Postgres console

# In the Postgres console
postgres=#    CREATE DATABASE social_distribution_db;           # Same as DB in settings.py
postgres=#    CREATE USER admin WITH PASSWORD 'password';       # Create user with a password
postgres=#    ALTER ROLE admin SET client_encoding TO 'utf8';   # Set encoding
postgres=#    ALTER ROLE admin SET default_transaction_isolation TO 'read committed';       # Set transaction
postgres=#    GRANT ALL PRIVILEGES ON DATABASE social_distribution_db TO admin;             # Allow user access to DB
postgres=#    \q # To exit console
```

# Admin Authentication

To login in to the admin page.
Run the following command from the root and add your user information.

```
python manage.py createsuperuser
```

# Django Project Structure
This Django project was created by loosely following this guide for file structure and organization:

https://studygyaan.com/django/best-practice-to-structure-django-project-directories-and-files

Apps are created in an apps folder to

To create a new app (for example, one called 'new_app'), first go to the *apps* folder via ```cd ../apps```.
Then run the following command from the *apps* folder:

```
python manage.py startapp new_app
```

Next, go into the file **apps.py** inside of the *new_app* directory and change the following: ```name = 'apps.new_app'```.
Lastly, add ```apps.appname``` to INSTALLED_APPS in **settings.py** of the *social_distribution* directory.





