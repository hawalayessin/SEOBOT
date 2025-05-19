# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install django psycopg2-binary requests

# Make port 8000 available to the world outside this container
EXPOSE 8000
