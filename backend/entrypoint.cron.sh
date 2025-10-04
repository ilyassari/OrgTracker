#!/bin/sh

# Check if the database is PostgreSQL and wait until it's available
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py crontab add

# Execute the command passed as arguments
exec "$@"
