FROM python:3.10.3-alpine3.14

ENV PYTHONUNBUFFERED 1

COPY ./requirement.txt ./requirement.txt
RUN pip install -r /requirement.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user