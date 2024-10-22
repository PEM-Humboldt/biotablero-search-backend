# Uses Python slim base image
FROM python:3.12-slim

# Establish the working directory
WORKDIR /app

# Install necessary packages, including unzip
RUN apt-get update && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Unzip Lambda layers directly in /opt (where Lambda expects the layers)
RUN unzip -o lambda_layer_heavy_part1.zip -d /opt
RUN unzip -o lambda_layer_heavy_part2.zip -d /opt
RUN unzip -o lambda_layer_heavy_part3.zip -d /opt
RUN unzip -o lambda_layer_heavy_part4.zip -d /opt

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
