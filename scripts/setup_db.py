#!/usr/bin/env python

import argparse
from pathlib import Path

import psycopg2
import os, dotenv
from psycopg2 import sql


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Set up the database for the portal.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop the database and user if they already exist, then recreate them.",
    )
    args = parser.parse_args()

    # Read env from backend/.env
    BASE_DIR = Path(__file__).resolve().parent.parent

    dotenv_file = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)

    # Read the host address and port from .env
    # If none is specified, localhost:5432 or UNIX domain sockets are used
    HOST = os.environ.get('404_DB_HOST', None)
    PORT = os.environ.get('404_DB_PORT', None)

    # Read name of database, user, and password to connect to the PostgreSQL server with
    PG_CONNECT_DB_NAME = os.environ.get("PG_CONNECT_DATABASE", "postgres")
    PG_CONNECT_USER = os.environ.get("PG_CONNECT_USER", "postgres")
    PG_CONNECT_PASSWORD = os.environ.get("PG_CONNECT_PASSWORD", "")

    # Read name of database, user, and password to create from .env
    DB_NAME = os.environ.get("404_DB_DATABASE")
    print(DB_NAME,"THEHTHTHTHTH")
    USER = os.environ.get("404_DB_USER")
    PASSWORD = os.environ.get("404_DB_PASSWORD")
    print(PASSWORD)

    # Connect to database named 'postgres'
    conn = psycopg2.connect(
        database=PG_CONNECT_DB_NAME,
        host=HOST,
        port=PORT,
        user=PG_CONNECT_USER,
        password=PG_CONNECT_PASSWORD,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if database already exists
    cursor.execute(
        """
    SELECT 1 FROM pg_catalog.pg_database WHERE datname=%s;
    """,
        (DB_NAME,),
    )
    database_already_exists = cursor.fetchone() is not None

    if database_already_exists and not args.reset:
        print(
            f'Database "{DB_NAME}" already exists. Run with --reset to drop and recreate it'
        )
    else:
        if database_already_exists:
            # Drop the database
            cursor.execute(
                sql.SQL(
                    """
            DROP DATABASE {db_name};
            """
                ).format(db_name=sql.Identifier(DB_NAME))
            )
            print(f'Successfully dropped database "{DB_NAME}"')

        # Create the database
        # This has to be separated from the rest of the statements,
        # otherwise the query gets run in a transaction, and we
        # can't create a database inside a transaction.
        print(DB_NAME,"TEST")
        cursor.execute(
            sql.SQL(
                """
        CREATE DATABASE {db_name};
        """
            ).format(db_name=sql.Identifier(DB_NAME))
        )
        print(f'Successfully created database "{DB_NAME}"')

    # Check if user already exists
    cursor.execute(
        """
    SELECT 1 FROM pg_roles WHERE rolname=%s;
    """,
        (USER,),
    )
    user_already_exists = cursor.fetchone() is not None

    if user_already_exists and not args.reset:
        print(f'User "{USER}" already exists. Run with --reset to drop and recreate it')
    else:
        if user_already_exists:
            # Drop the user
            cursor.execute(
                sql.SQL(
                    """
            DROP USER {user};
            """
                ).format(user=sql.Identifier(USER))
            )
            print(f'Successfully dropped user "{USER}"')

        # Create user, set password, configuration for Django, and grant privileges
        # User will have all privileges on the created database
        # They will also be allowed to create databases, as this is needed for testing
        # https://docs.djangoproject.com/en/3.2/ref/databases/#optimizing-postgresql-s-configuration
        cursor.execute(
            sql.SQL(
                """
        CREATE USER {user};
        ALTER USER {user} WITH ENCRYPTED PASSWORD {password};
        ALTER USER {user} SET client_encoding='UTF-8';
        ALTER USER {user} SET default_transaction_isolation='read committed';
        ALTER USER {user} SET timezone='UTC';
        ALTER USER {user} createdb;
        GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};
        """
            ).format(
                db_name=sql.Identifier(DB_NAME),
                user=sql.Identifier(USER),
                password=sql.Literal(PASSWORD),
            )
        )
        print(f'Successfully created user "{USER}"')

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
