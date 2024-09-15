FROM python:3.11

RUN apt-get update
RUN apt-get install -y netcat-traditional

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt /app

RUN pip install -r requirements.txt

# Bundle app source
COPY . /app
