#!/bin/bash
# server-start.sh
# you can pass in
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd app; python manage.py createsuperuser --no-input)
fi
(cd app; gunicorn app.wsgi:application --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
(cd app; python manage.py collectstatic --no-input)
(cd app; python manage.py migrate --no-input)
