FROM python:3.9.1-alpine

ENV PYTHONUNBUFFERRED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

# Necessary psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev	

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY clinic /code/


