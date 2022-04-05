# mcc-alexa-app

[![CircleCI](https://circleci.com/gh/Mobilise-Devlopment/client-project-1/tree/development.shield?style=svg)](https://circleci.com/gh/Mobilise-Devlopment/client-project-1/tree/development)

# Current requirements

Can be found in the [requirements.txt](../requirements.txt") file in the cms root folder

# Core

The core application is the central location where management commands and any required fixtures for the project should
be placed.

## Environment Variables (Required)

|  Variable |Type   |Value   | Purpose|
|---|---|---|---|
| CMS_DEBUG  | String  | "True" or "False"   |Running the project in DEBUG mode, should be False in production|
| CMS_SECURE_HSTS_SECONDS  | String  | "0" or another integer value as a string  | Represents the number of seconds before browser should check again|
| CMS_SECURE_HSTS_INCLUDE_SUBDOMAINS  | String  | "True" or "False"   | True requires subdomains to also redirect to SSL |
| CMS_SECURE_HSTS_PRELOAD  | String  | "True" or "False"   |reload none secure request as secure requests|
| CMS_SESSION_COOKIE_SECURE  | String  | "True" or "False"   | set to True to secure cookies|
| CMS_SECURE_SSL_REDIRECT  | String  | "True" or "False"   | Redirect non secure|
| CMS_CSRF_COOKIE_SECURE  | String  | "True" or "False"   |Send CSRF cookie securely|
| CMS_ALLOWED_HOSTS  | String  | Comma seperated list   | for example "localhost, mydomain.com" |
| CMS_SECRET_KEY  | String  | unique key  | to be used as as per DJANGO SECRET_KEY |
| CMS_STATIC_ROOT| String | Path | Set to any empty string to use basedir with default folder|
| CMS_MEDIA_ROOT| String | Path | Set to any empty string to use basedir with default folder|
| POSTGRES_DB_HOST| String | Path | |
| POSTGRES_DB_NAME| String | Path | Set to any empty string to use basedir with default folder|
| POSTGRES_DB_USER| String | Path | Set to any empty string to use basedir with default folder|
| POSTGRES_DB_PASS| String | Path | Set to any empty string to use basedir with default folder|
| REDIS_HOST| String | Path | Set to any empty string to use basedir with default folder|
| REDIS_ENV_PREFIX| String | Path | Set to any empty string to use basedir with default folder|


## Building and Running the application
For development, you can run the app as is using the standard `python manage.py runserver` command.However, you will need
to have the required depedencies installed.

1. Postgres
2. Redis

You'll need to load the required environment variables as listed [environment variables](#environment-variables-required)
either in to your python environment directly or (preferred for local dev) in to a `.env` file). For the latter, we're using
[Python Decouple](https://pypi.org/project/python-decouple/) to simplify how environment variables are managed. It offers 
convenient methods managing environment variables of differernt types and looks for them in the following order 1. The environment 2. The .env file 3rd it'll using the default value if one was passed in for example:
   
    EMAIL_HOST = config('EMAIL_HOST', default='localhost')


Once you have those setup create a virtual environment to install your pacage depedencies in to:

    # Create a virtual env
    `virtualenv -ppython3 .venv`

    # Activate the virtual env
    `source .venv/bin/activate`
    
    # Install the requirements for the project 
    `pip install -r requirements.txt`
    
    # Run migrations fort the project
    `python manage.py migrate`

    # Start the application
    `python manage.py runserver`

This will start the application, you will need to have installed locally or configured in the .env hosts for the redis
and Postgres servers to be used with the application.

#### Option 2

##### Docker

The application is also configured to run in a container. Using the container the application will be deployed behind
NGINX and will be run using gunicorn (for more info lookup these applications)

For further info on the configuration review the `Dockerfile`

Dependencies:

- `start-server.sh`
- Postgres Server 
- Redis Server

build the container

    docker build -t cms .

run the container

    docker run -it -p 8020:8020 cms

Once running you can navigate to `localhost:8020`

Not the output in the console will point you towards port `0.0.0.0:8010` this is the the django app is running on
however you will access it through NGINX on port `8020`
is accessible.

---

#### Option 3

#### Docker Compose

As per Option 2 tha application setup is the same and leverages the files referenced there

However, docker composed is used to also deploy the other required services, such as Redis and Postgres

Specifics can be found here: 

    docker-compose.yml

In production, you're unlikely to want to deploy the additional services, however, in dev this enables you to run a
production like environment locally and is the least amount of effort overall.

To run the containers:

    docker compose up --build


---






#AWS docker container registry commands

Make sure that you have the latest version of the AWS CLI and Docker installed. For more information, see Getting Started with Amazon ECR .
Use the following steps to authenticate and push an image to your repository. For additional registry authentication methods, including the Amazon ECR credential helper, see Registry Authentication .
Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

    aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 243218137774.dkr.ecr.eu-west-2.amazonaws.com

Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.
Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:
    
    docker build -t mcc-alexia-app .

After the build completes, tag your image so you can push the image to this repository:

    docker tag mcc-alexia-app:latest 243218137774.dkr.ecr.eu-west-2.amazonaws.com/mcc-alexia-app:latest

Run the following command to push this image to your newly created AWS repository:
    
    docker push 243218137774.dkr.ecr.eu-west-2.amazonaws.com/mcc-alexia-app:latest
