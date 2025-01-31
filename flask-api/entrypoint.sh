#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "postgres has started started"

# run migrations
python manage.py db upgrade

# create test data
python manage.py init_dev_db

exec "$@"