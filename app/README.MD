# Current requirements

Can be found in the [requirements.txt](../requirements.txt") file in the cms root folder


# Email templates - MJML

Email templates are written using MJML, a HTML templating engine.

[The mjml docs](https://mjml.io/)

Install the mjml library

    pip install mjml    

Install the Pycharm plugin for MJML

    preferences > plugins > install MJML

Using the Pycharm plugin you can now use the MJML editor to create your email templates.

# Tasks - Workers
The application uses Celery and Redis to schedule tasks.
We have on demand tasks that are run on the first available worker and Scheduled tasks that are run on a cron schedule.
Emails are sent using aws ses.

The Scheduled tasks run every 5 minutes checking events to send on reminder of events due to start in the next 15 minutes.

To ensure the scheduled tasks are running you must run the Beat worker

    celery -A app beat -l INFO

To ensure on demand tasks are running you must run the worker

    celery -A app worker -l INFO

NB: The beat worker will in our app schedule the on demand tasks so both must be running for those scheduled tasks to run.

