# CMPUT404-project-socialdistribution

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

# CMPUT 404 Winter 2021 Team 6

    Fraser Redford
    Jawad Rizvi
    Mustafa Khairullah
    Ryan Kang
    Tim Van Maaren

# Environment Setup

Setup python virtual environment

```
virtualenv venv --python=python3.6
source venv/bin/activate
pip install -r requirements.txt
```

Create a secret_settings.py file inside manager/ because it is gitignored.
Inside, add:

```
KONNECT_SECRET_KEY = 'secret key'
```

Install the npm packages for the frontend:

```
npm install
```

You should now be able to run the code

```
cd manager
python manage.py runserver
```

If you want to run the frontend, type this from the root of the repo:

```
npm run dev
```

# Contributors / Licensing

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
