# Use Python 3.10 slim image
FROM public.ecr.aws/docker/library/python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for GDAL, GEOS, PROJ (needed for rasterio, geopandas)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdal-dev \
    gdal-bin \
    libgeos-dev \
    libproj-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./start.sh"]