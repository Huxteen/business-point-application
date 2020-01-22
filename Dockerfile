FROM python:3.7-alpine
MAINTAINER Husteen

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app


# used to run out processes from our project
# used for security process
RUN adduser -D user
USER user