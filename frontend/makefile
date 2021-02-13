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
