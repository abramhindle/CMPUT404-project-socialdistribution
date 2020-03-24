Welcome to our CMPUT404 Project Page!

Group Members: [Xiaole Zeng](https://github.com/XiaoleZ), [Will Fenton](https://github.com/willfenton), [Gregory Neagu](https://github.com/gneagu), [Muhammad Khan](https://github.com/um4r12), [Heyue Huang](https://github.com/JohnDoeMask)

Class Section: CMPUT 404 Winter 2020

CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

* superuser info:
```
usrname:cmput404w20t05@gmail.com
password:demo
```
* API endpoint: [API Documentation](https://github.com/CMPUT404W20Project/CMPUT404-project-socialdistribution/wiki/API-Documentation)

Setup guide
===========
1. Create an empty directory and cd into it
2. Setup virtualenv
3. Activate virtualenv
4. Clone repository
5. Pip install requirements
6. Run django server

```
mkdir social-distribution-project && cd social-distribution-project
virtualenv venv --python=python3
source venv/bin/activate
git clone https://github.com/CMPUT404W20Project/CMPUT404-project-socialdistribution.git
cd CMPUT404-project-socialdistribution
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Migrations were causing an issue, and the old migrations and db may need to be reset. If errors occur, from the project directory, do the following:
 
```
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
mv db.sqlite3 db.sqlite3.bk
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

How to run
========================
1. Setup virtualenv
2. Activate virtualenv
3. Clone repository
4. Navigate to socialdistribution
5. Pip install requirements
6. Run django server

```
virtualenv venv --python=python3
source venv/bin/activate
git clone https://github.com/CMPUT404W20Project/CMPUT404-project-socialdistribution.git
cd CMPUT404-project-socialdistribution
cd socialdistribution
pip install -r requirements.txt
python manage.py runserver
```
7. Run tests
⚠️testsui.py requires geckodriver. Unfortunately it can't be installed via pip, if you would like to run the ui tests
please download geckodriver manually [geckodriver](https://github.com/mozilla/geckodriver/releases) and add it to your virtualenv(under venv/bin) ⚠️
```
python3 manage.py test
```
Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

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
