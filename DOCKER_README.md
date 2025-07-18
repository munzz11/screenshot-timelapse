# Docker Timelapse Generator

This directory contains Docker configuration for running the timelapse generator in a container with scheduled execution.

## Quick Start

### 1. Set your screenshots path

Copy the example environment file and set your path:

```bash
cp env.example .env
```

Edit `.env` and set your screenshots directory:
```bash
SCREENSHOTS_PATH=/path/to/your/screenshots
```

### 2. Build and run

```bash
# Build the container
docker-compose build

# Start the service
docker-compose up -d
```

The container will:
- Run timelapse generation immediately when started
- Then run every hour automatically
- Restart automatically if stopped

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SCREENSHOTS_PATH` | Path to your screenshots directory | `./screenshots` |

### Scheduling

The container runs timelapse generation:
- **Immediately** when the container starts
- **Every hour** after that (at the top of each hour)

The schedule is built into the container and cannot be changed without rebuilding.

## Usage Examples

### Basic Setup

```bash
# 1. Set your screenshots path
echo "SCREENSHOTS_PATH=/home/user/screenshots" > .env

# 2. Start the service
docker-compose up -d

# 3. Check logs
docker-compose logs -f
```

### Multiple Screenshots Directories

If you have multiple directories to process, you can run multiple containers:

```bash
# Create separate .env files for each directory
echo "SCREENSHOTS_PATH=/path/to/directory1" > .env.dir1
echo "SCREENSHOTS_PATH=/path/to/directory2" > .env.dir2

# Run separate containers
docker-compose --env-file .env.dir1 up -d
docker-compose --env-file .env.dir2 up -d
```

## Monitoring

### View Logs

```bash
# View recent logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs from the last 24 hours
docker-compose logs --since 24h
```

### Check Container Status

```bash
# Check if container is running
docker-compose ps

# Check container resource usage
docker stats timelapse-generator
```

### Manual Execution

```bash
# Run the script manually inside the container
docker-compose exec timelapse-generator python3 simple_timelapse.py /data
```

## Troubleshooting

### Container Won't Start

```bash
# Check for errors
docker-compose logs

# Verify the screenshots path exists and is accessible
ls -la /path/to/your/screenshots
```

### Permission Issues

If you encounter permission issues:

```bash
# Check file permissions
ls -la /path/to/your/screenshots

# Ensure the directory is readable
chmod 755 /path/to/your/screenshots
```

### Schedule Not Working

```bash
# Check if cron is running
docker-compose exec timelapse-generator ps aux | grep cron

# Check cron logs
docker-compose exec timelapse-generator tail -f /var/log/timelapse.log
```

### Disk Space Issues

```bash
# Check available disk space
docker-compose exec timelapse-scheduler df -h

# Clean up old containers and images
docker system prune -f
```

## Security Notes

- The container runs as a non-root user (`timelapse`)
- Screenshots directory is mounted as read-only (`:ro`)
- Container restarts automatically unless explicitly stopped
- Logs are written to `/var/log/timelapse.log` inside the container

## Performance Considerations

- The container uses up to 8 parallel processes for timelapse generation
- Memory usage depends on image sizes and number of screenshots
- Consider running during off-peak hours for large repositories
- Monitor disk space as timelapses are generated in the original directory structure 