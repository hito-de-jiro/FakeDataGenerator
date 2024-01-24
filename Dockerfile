FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY app /app
WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk add postgresql-client build-base postgresql-dev

RUN python -m pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user
