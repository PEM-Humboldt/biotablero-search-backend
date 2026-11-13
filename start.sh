#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
  echo "Waiting for database to be ready... $DB_HOST:$DB_PORT"
  nc -z $DB_HOST $DB_PORT
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
aerich upgrade

# Populate database (only when explicitly requested)
if [ "$RUN_SEED" = "true" ]; then
  echo "Populating database..."
  python -m database.populate_db
else
  echo "Skipping DB populate (set RUN_SEED=true to enable)"
fi

# Start the application
echo "Starting the application..."
if [ "$RELOAD" = "1" ]; then
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
  uvicorn app.main:app --host 0.0.0.0 --port 8000
fi