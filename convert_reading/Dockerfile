# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies
RUN pip install --no-cache-dir google-cloud-pubsub

# Run convert_reading.py when the container launches
CMD ["python", "convert_reading.py"]