# pull official base image
FROM python:3.8.5-alpine

RUN apk update \
    && apk add --virtual build-deps \
    postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg \
    tzdata

ENV PROJECT_DIR /usr/src/grocerfinder_root

# set work directory
WORKDIR ${PROJECT_DIR}

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv==2020.8.13
COPY ./Pipfile ./Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE postgres
ENV DJANGO_SETTINGS_MODULE=grocerfinder.settings.production

# Set to True if wanting to Flush data upon container init. 
# Warning will delete current data
ENV DJANGO_FLUSH_DATA=False

# Set to True if wanting to Flush data upon container init. 
ENV DJANGO_MIGRATE=False

# Set to True if loading data from data.json file
ENV DJANGO_LOAD_DATA=False

ENV TZ=America/New_York


# copy entrypoint.sh
COPY ./entrypoint.sh ${PROJECT_DIR}

# copy project
COPY ./grocerfinder_root .

# run entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]