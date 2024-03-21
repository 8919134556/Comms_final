# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/app/alarm_4050

# Copy specific files into the container
COPY src /usr/app/alarm_4050/src
COPY test /usr/app/alarm_4050/test
COPY requirements.txt /usr/app/alarm_4050

# Install required packages, including the SQL Server ODBC driver and gnupg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        unixodbc \
        unixodbc-dev \
        curl \
        gnupg && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Microsoft package repository for msodbcsql17
RUN curl -fsSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update package lists again and install msodbcsql17
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for persistent data
VOLUME /usr/app/alarm_4050/Alarm_4050_logs

# Expose port 8012
EXPOSE 8012

# Run main.py when the container launches
CMD ["python", "./src/main.py"]
