psql -U postgres -d postgres -c "DROP DATABASE social_distribution_db;"
psql -U postgres -d postgres -c "CREATE DATABASE social_distribution_db;"
psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE social_distribution_db to admin;"
