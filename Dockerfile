# Pull the official base image
FROM python:3.9.1-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./clinic /app

# Set the work directory
WORKDIR /app

COPY ./entrypoint .sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

# Set the environment variables
# PYTHONDONTWRITEBYTECODE prevents Python from copying pyc files to the container
# PYTHONUNBUFFERED ensures that Python output is logged to the terminal, making it possible to monitor django in 
# real time
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERRED 1

