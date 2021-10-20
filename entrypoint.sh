#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "Postgres started"

    # flush data if needed
    if [ "$DJANGO_FLUSH_DATA" = "True" ]
    then 
        python manage.py flush --no-input
        echo "data flushed"
    fi

    # migrate if needed
    if [ "$DJANGO_MIGRATE" = "True" ]
    then
        python manage.py migrate --no-input
        echo "django migrated"
    fi
    
    if [ $DJANGO_SUPERUSER_PASSWORD ]
    then
        python manage.py createsuperuser --noinput \
            --username grocerfinder_root \
            --email admin@grocerfinder.com
    fi
    if [ $DJANGO_LOAD_DATA ]; then
        python manage.py loaddata data.json
    fi
fi
exec "$@"