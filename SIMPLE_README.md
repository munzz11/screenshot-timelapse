# Simple Timelapse Generator

A minimal tool to create timelapses from screenshot repositories.

## What it does

- Takes a path to your screenshots folder
- Finds all workstations and dates automatically
- Creates a 24 FPS timelapse for each day
- Creates a timelapses/ folder under each workstation and saves timelapses there
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

## Installation

```bash
pip3 install -r simple_requirements.txt
```

## Usage

### Option 1: Python script
```bash
python3 simple_timelapse.py /path/to/screenshots
```

### Option 2: Shell script
```bash
chmod +x simple_timelapse.sh
./simple_timelapse.sh /path/to/screenshots
```

## Output

Timelapses will be saved in a timelapses/ folder under each workstation:
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

- ✅ 24 FPS fixed rate
- ✅ Processes all PNG files in each date folder
- ✅ Sorts images by filename
- ✅ Progress bars for each timelapse
- ✅ **Smart regeneration** - only recreates timelapses when screenshots change
- ✅ **Hash tracking** - remembers which screenshots were used for each timelapse
- ✅ **Time-based checking** - detects when new screenshots are added
- ✅ **Parallel processing** - processes multiple days simultaneously (up to 8 processes)
- ✅ Simple error handling
- ✅ Minimal dependencies (just OpenCV and tqdm)

That's it! Simple and focused. 