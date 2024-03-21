# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/app/alarm_4050

# Copy specific files into the container
COPY src /usr/app/alarm_4050/src
COPY test /usr/app/alarm_4050/test
COPY requirements.txt /usr/app/alarm_4050

# Install required packages, including the SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc unixodbc-dev curl && \
    if ! apt-key list | grep -q "Microsoft (Release signing)"; then \
        apt-get install -y gnupg && \
        curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -; \
    fi && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    msodbcsql17 && \
    pip install --no-cache-dir -r requirements.txt

# Create a volume for persistent data
VOLUME /usr/app/alarm_4050/Alarm_4050_logs

# Expose port 8012
EXPOSE 8012

# Run alarm_processor.py when the container launches
CMD ["python", "./src/main.py"]
