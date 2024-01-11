# pull official base image
FROM python:3

RUN pip install pipenv
# copy project
COPY app /app
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY Pipfile* /app/
RUN pipenv install --system --deploy --ignore-pipfile
ADD app /app/