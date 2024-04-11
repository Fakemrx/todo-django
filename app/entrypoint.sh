#!/bin/sh

if [ "$POSTGRES_DB" = "postgres" ]
  then
    echo "Waiting for psql"
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1
      echo "PSQL still launching"
    done
fi

python manage.py migrate

exec "$@"