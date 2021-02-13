# Run a docker container
compose-start:
	docker-compose up --remove-orphans $(options)

# Run a docker container in detached mode so it does not block the terminal
compose-start-detached:
	docker-compose up -d --remove-orphans $(options)

# Stop the running docker container and remove it
# Note: If you wish to delete docker volume run this command with the option -v
compose-stop:
	docker-compose down --remove-orphans $(options)

# Run migrations to persist to database
compose-migrate:
	docker-compose exec web python manage.py migrate

# Make migrations
compose-make-migrations:
	docker-compose exec web python manage.py makemigrations

# Run any command in a new container
compose-manage-py:
	docker-compose run --rm $(options) web python manage.py $(cmd)


