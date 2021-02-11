# Backend Structure
***Using the Django Framework***
```
backend
├── manage.py
├── requirements.txt
├── readme.md
├── socialdistribution (Project)
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api (App)
    ├── admin.py
    ├── apps.py
    ├── tests.py
    ├── views (Directory to contain all explicity named views)
    └── models (Directory to contain all explicity named models)

```

## Getting Started
* Assume all commands are being run from within the `backend/` directory
### Create A Virtual Environment and Activate
```python
python3 -m venv venv
source venv/bin/activate
```

### Database
* `postgresql` is the database of choice for this project
* Make sure to install it for your platform Windows, Mac or Linux
* Note: You must create a database in postgresql for local development prior to continuing
##### Setup on Django
- In the backend folder
    - `touch .env` (Creates an environment variable file)
    -  In the `.env` file add in a postgresql connection string in the following format: `DATABASE_URL=postgresql://localhost/test404?user=myname&password=mypassword
`

### Install Requirements
* Remember to add to requirements.txt any requirements needed for the backend, so any other user can easily install them.
```python
pip install -r requirements.txt
```

### Conventions
- `views` 
    - This directory should contain views separated based on resource.It should be based on whatever resource or actions it pertains to.
    - Example: author or comments related endpoints should reside in `author.py` and `comments.py` respectively.
- `models`
    - Contains models separated by database tables
    - Example: author should be `author.py`

## Run the Server
```python
python manage.py runserver
```

