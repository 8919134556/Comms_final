# Use an official Python runtime as a parent image
FROM python:3.9.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy specific files into the container
COPY src /usr/src/app/

# Install required packages, including the SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends unixodbc unixodbc-dev curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY src/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for persistent data
VOLUME /usr/src/app/logs

# Expose port 8011
EXPOSE 8011

# Run main.py when the container launches
CMD ["python3", "./src/main.py"]
