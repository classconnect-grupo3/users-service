# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-cov pytest-asyncio

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE ${PORT}

# Command to run the application
CMD uvicorn app.main:app --host ${HOST} --port ${PORT} --reload