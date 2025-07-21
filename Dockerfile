FROM python:3.11-slim

# Install system dependencies including cron
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the timelapse script
COPY timelapse.py .

# Create a non-root user
RUN useradd -m -u 1000 timelapse && \
    chown -R timelapse:timelapse /app

# Install Python packages for the timelapse user
USER timelapse
RUN pip install --user --no-cache-dir -r /app/requirements.txt
USER root

# Create a startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'echo "Timelapse generator starting..."' >> /app/start.sh && \
    echo 'echo "Screenshots path: $SCREENSHOTS_PATH"' >> /app/start.sh && \
    echo 'echo "Current time: $(date)"' >> /app/start.sh && \
    echo 'su timelapse -c "python3 /app/timelapse.py /data"' >> /app/start.sh && \
    echo 'echo "Timelapse generation complete at $(date)"' >> /app/start.sh && \
    echo 'echo "Setting up cron for hourly runs..."' >> /app/start.sh && \
    echo 'echo "0 * * * * su timelapse -c \"cd /app && python3 timelapse.py /data\" >> /var/log/timelapse.log 2>&1" | crontab -' >> /app/start.sh && \
    echo 'echo "Starting cron daemon for hourly execution..."' >> /app/start.sh && \
    echo 'service cron start' >> /app/start.sh && \
    echo 'touch /var/log/timelapse.log' >> /app/start.sh && \
    echo 'echo "Container started at $(date)" >> /var/log/timelapse.log' >> /app/start.sh && \
    echo 'echo "Waiting for hourly timelapse generation..."' >> /app/start.sh && \
    echo 'tail -f /var/log/timelapse.log' >> /app/start.sh && \
    chmod +x /app/start.sh

# Set the default command
CMD ["/app/start.sh"] 