# Use an official Python runtime as a parent image
FROM python:3.9.9-slim

# Set the working directory in the container
WORKDIR /usr/app/gps_4040

# Copy the application source code and requirements file into the container
COPY src /usr/app/gps_4040/src
COPY test /usr/app/gps_4040/test
COPY requirements.txt /usr/app/gps_4040

# Install required packages, including the SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        unixodbc \
        unixodbc-dev \
        curl \
        gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for persistent data
VOLUME /usr/app/gps_4040/logs

# Expose port 8011
EXPOSE 8011

# Run main.py when the container launches
CMD ["python", "./src/main.py"]
