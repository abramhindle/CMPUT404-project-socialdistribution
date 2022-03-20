## Requirements

- Python 3.9.10

## Quick start

1. Clone the repo
   ```sh
   mkdir socialdistribution
   git clone git@github.com:CMPUT404W22AMNRY/CMPUT404-project-socialdistribution.git socialdistribution
   cd socialdistribution
   ```
2. Create a new virtual environment
   ```sh
   python3 -m venv venv
   ```
3. Activate virtual environment
   ```sh
   source ./venv/bin/activate
   ```
4. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
5. Run server
   ```sh
   python manage.py runserver
   ```

## Testing multiple servers

We can run multiple independent servers using Docker to test the distributed aspect of the project

1. Build the container
   ```sh
   docker build -t socialdistribution .
   ```
2. Run the container in detached mode
   ```sh
   docker run --rm -p 8001:8000 --name socialdistribution -d socialdistribution
   ```
3. Stop the container when you're done
   ```sh
   docker kill socialdistribution
   ```
