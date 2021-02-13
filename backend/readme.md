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
### Create A Virtual Environment and Activate (Optional step)
```python
python3 -m venv venv
source venv/bin/activate
```

### Database
* `postgresql` is the database of choice for this project

##### Setup on Django
- In the backend folder
    - `touch .env` (Creates an environment variable file)
    - This `.env` file is essential to define the credentials for the database that will be created and persisted by docker
    - Example: (Keep everything the same except the password)
    ``` 
     POSTGRES_DB=mydb_dev
     POSTGRES_NAME=mydb_dev
     POSTGRES_USER=coolusername
     POSTGRES_PASSWORD=password
     DEBUG=1
    ```

### Requirements
* Ensure you have both `docker` and `docker-compose` installed on your machine

### Run Application and Docker Considerations
* All relevant commands to run the application are present in the `Makefile`
* To start up the application, run: `make compose-start`
    * This will start the application and create a persistent postgresql database
    * This will show you all logs of the app while running. If you do not want to see these, you can run the docker in a detached state by using: `make compose-start-detached`
* To stop the docker container run: `make compose-stop`
* In order to makemigrations or apply migrate, run: `make compose-manage-py cmd="<enter your command here>"`

### View Database
* In order to view the database from the command line you must perform the following steps:
    1. Ensure application is running with `make compose-start`
    2. Enter Bash of Database container with `make compose-db-bash`
    3. In the bash enter: `psql -h db <db-name> -d <user-name>`

### Conventions
- `views` 
    - This directory should contain views separated based on resource.It should be based on whatever resource or actions it pertains to.
    - Example: author or comments related endpoints should reside in `author.py` and `comments.py` respectively.
- `models`
    - Contains models separated by database tables
    - Example: author should be `author.py`

