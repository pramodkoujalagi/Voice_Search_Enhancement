# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    portaudio19-dev

# Upgrade pip, setuptools, and wheel
RUN pip3 install --upgrade pip setuptools wheel

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --use-deprecated=legacy-resolver -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the command to run your application
CMD ["python3", "app.py"]
