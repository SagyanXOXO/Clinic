# Pull the official base image
FROM python:3.9.1-alpine

# Set the work directory
WORKDIR /app

# Set the environment variables
# PYTHONDONTWRITEBYTECODE prevents Python from pyc files to the container
# PYTHONUNBUFFERED ensures that Python output is logged to the terminal, making it possible to monitor django in 
# real time
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERRED 1

# install dependencies
RUN pip install --upgrade pip
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the project
COPY clinic /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]