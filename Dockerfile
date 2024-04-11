FROM python:3.11.7-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt install -y netcat-traditional
RUN pip install --upgrade pip
RUN pip install -U pipenv

COPY app /usr/src/app
COPY Pipfile Pipfile.lock /usr/src/app/

RUN pipenv install --system

RUN chmod +x ./entrypoint.sh

EXPOSE 8000
