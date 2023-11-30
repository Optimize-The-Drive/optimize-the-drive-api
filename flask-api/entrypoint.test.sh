#!/bin/sh

# 
# Script doesn't differ from entrypoint.sh, but
# will diverge once we start adding mock data.
#

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "postgres has started started"

# run migrations
python manage.py db upgrade

# create test data
python manage.py init_db

exec "$@"