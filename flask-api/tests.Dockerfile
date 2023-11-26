FROM python:3-alpine

# Create app directory
WORKDIR /app

# Copy pylint file into container
COPY ../.pylintrc ./

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 5000
CMD ["pytest"]
