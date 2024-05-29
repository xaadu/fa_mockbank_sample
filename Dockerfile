# Use the official Python image as the base image
FROM python:3.12.2-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Run the application
CMD ["python", "app.py"]
