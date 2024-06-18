# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install required packages for building C code and SWIG
RUN apt-get update && apt-get install -y build-essential clang swig

# Copy the current directory contents into the container at /app
COPY . /app

# Build the C code using makefile
RUN make

# Set the environment variable for the shared library
ENV LD_LIBRARY_PATH /app

# Install any needed packages specified in setup.py
RUN pip install .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python", "server.py"]
