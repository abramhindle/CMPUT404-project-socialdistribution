CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

Prerequisites
=============
Following packages are required for python

<b>Django</b> `pip install Django`

<b>Markdown</b>:  `pip install django-markdown-deux`

Install
=======
To run the server: `cd socialdistribution; python manage.py runserver`

Changing the Models
===================
To update the Django database to reflect latest model changes, run:

    $ python manage.py makemigrations <app>
    $ python manage.py migrate

Creating an Admin
===============
To create a admin, do the following:

    $ python manage.py createsuperuser

Fill in the prompted information, start the server, and go to localhost:8000/admin to create an author.


Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Jim Wen
    Jessica Yuen
    Nhu Bui
    Valerie Sawyer
    Lin Tong
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
