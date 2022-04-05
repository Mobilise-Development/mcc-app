FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
RUN apt-get install gunicorn -y
RUN apt-get install python3-pip -y

COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p app
RUN mkdir -p app/pip_cache
COPY requirements.txt server-start.sh /app/
COPY .pip_cache /app/pip_cache/
COPY app /app/
WORKDIR /app/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic
RUN chown -R www-data:www-data /mcc-alexa/app

EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/mcc-alexa/server-start.sh"]