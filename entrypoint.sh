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
    
    # create super user if password set
    if [ $DJANGO_SUPERUSER_PASSWORD ]
    then
        python manage.py createsuperuser --noinput \
            --username grocerfinder_root \
            --email admin@grocerfinder.com
    fi
    
    # load data if needed
    if [ $DJANGO_LOAD_DATA ]; then
        python manage.py loaddata data.json
    fi
    
    # create user1 for visitor
    python manage.py shell --command="
from django.contrib.auth import get_user_model;
UserModel = get_user_model();
if not UserModel.objects.filter(username='user1').exists():
    user=UserModel.objects.create_user('user1', password='user1')
    user.save();
else:
    print('user1 existed');


exit()
"
fi
exec "$@"