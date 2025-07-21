# Timelapse Generator

A minimal tool to create timelapses from screenshot repositories, with support for both local and Dockerized execution.

---

## What it does
- Takes a path to your screenshots folder
- Finds all workstations and dates automatically
- Creates a 24 FPS timelapse for each day
- Creates a `timelapses/` folder under each workstation and saves timelapses there
- **Smart regeneration**: Only recreates timelapses when screenshots have changed
- **Parallel processing**: Processes multiple days simultaneously for faster generation

## Directory Structure
Your screenshots should be organized like this:
```
screenshots_path/
├── Roc1Pilot/
│   ├── 2025-06-29/
│   │   ├── screenshot1.png
│   │   ├── screenshot2.png
│   │   └── ...
│   └── 2025-07-02/
│       └── ...
└── Roc1Survey/
    ├── 2025-07-05/
    │   └── ...
    └── ...
```

## Local Usage

### Installation
```bash
pip3 install -r requirements.txt
```

### Run as Python script
```bash
python3 timelapse.py /path/to/screenshots
```

### Run as Shell script
```bash
chmod +x timelapse.sh
./timelapse.sh /path/to/screenshots
```

## Output
Timelapses will be saved in a `timelapses/` folder under each workstation:
```
screenshots_path/
├── Roc1Pilot/
│   ├── timelapses/
│   │   ├── Roc1Pilot_2025-06-29_timelapse.mp4
│   │   ├── Roc1Pilot_2025-07-02_timelapse.mp4
│   │   ├── .Roc1Pilot_2025-06-29_timelapse.hash
│   │   └── .Roc1Pilot_2025-07-02_timelapse.hash
│   ├── 2025-06-29/
│   │   └── (screenshots...)
│   └── 2025-07-02/
│       └── (screenshots...)
└── Roc1Survey/
    ├── timelapses/
    │   ├── Roc1Survey_2025-07-05_timelapse.mp4
    │   └── .Roc1Survey_2025-07-05_timelapse.hash
    └── 2025-07-05/
        └── (screenshots...)
```

**Note:** Each timelapse has a corresponding hidden `.hash` file that tracks which screenshots were used to create it.

## Features
- 24 FPS fixed rate
- Processes all PNG files in each date folder
- Sorts images by filename
- Progress bars for each timelapse
- **Smart regeneration** - only recreates timelapses when screenshots change
- **Hash tracking** - remembers which screenshots were used for each timelapse
- **Time-based checking** - detects when new screenshots are added
- **Parallel processing** - processes multiple days simultaneously (up to 8 processes)
- Simple error handling
- Minimal dependencies (just OpenCV and tqdm)

---

# Docker Usage

This project includes Docker configuration for running the timelapse generator in a container with scheduled execution.

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
docker-compose build
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
echo "SCREENSHOTS_PATH=/home/user/screenshots" > .env
docker-compose up -d
docker-compose logs -f
```

### Multiple Screenshots Directories
If you have multiple directories to process, you can run multiple containers:
```bash
echo "SCREENSHOTS_PATH=/path/to/directory1" > .env.dir1
echo "SCREENSHOTS_PATH=/path/to/directory2" > .env.dir2
docker-compose --env-file .env.dir1 up -d
docker-compose --env-file .env.dir2 up -d
```

## Monitoring

### View Logs
```bash
docker-compose logs
docker-compose logs -f
docker-compose logs --since 24h
```

### Check Container Status
```bash
docker-compose ps
docker stats timelapse-generator
```

### Manual Execution
```bash
docker-compose exec timelapse-generator python3 timelapse.py /data
```

## Troubleshooting

### Container Won't Start
```bash
docker-compose logs
ls -la /path/to/your/screenshots
```

### Permission Issues
```bash
ls -la /path/to/your/screenshots
chmod 755 /path/to/your/screenshots
```

### Schedule Not Working
```bash
docker-compose exec timelapse-generator ps aux | grep cron
docker-compose exec timelapse-generator tail -f /var/log/timelapse.log
```

### Disk Space Issues
```bash
docker-compose exec timelapse-scheduler df -h
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