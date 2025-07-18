#!/usr/bin/env python3
"""
Simple Timelapse Generator

Creates timelapses for each day in a screenshot repository.
Assumes structure: screenshots_path/workstation/date/*.png
"""

import os
import sys
import hashlib
from pathlib import Path
import cv2
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

def get_image_hash(image_path):
    """Get a hash of the image file (size + modification time)."""
    stat = image_path.stat()
    return f"{stat.st_size}_{stat.st_mtime}"

def get_images_hash(image_files):
    """Get a combined hash of all image files."""
    # Create a deterministic hash by sorting filenames and combining hashes
    sorted_files = sorted(image_files, key=lambda x: x.name)
    hash_string = "|".join(get_image_hash(img) for img in sorted_files)
    return hashlib.md5(hash_string.encode()).hexdigest()

def needs_regeneration(image_files, output_path):
    """Check if timelapse needs to be regenerated."""
    if not output_path.exists():
        return True
    
    # Check if the timelapse file is newer than all images
    timelapse_mtime = output_path.stat().st_mtime
    newest_image_mtime = max(img.stat().st_mtime for img in image_files)
    
    if timelapse_mtime < newest_image_mtime:
        return True
    
    # Check if we have a hash file to compare
    hash_file = output_path.parent / f".{output_path.stem}.hash"
    if hash_file.exists():
        try:
            with open(hash_file, 'r') as f:
                stored_hash = f.read().strip()
            current_hash = get_images_hash(image_files)
            
            if stored_hash != current_hash:
                return True
            else:
                return False
        except:
            return True
    else:
        return True

def create_timelapse(image_files, output_path, fps=24):
    """Create a timelapse from a list of image files."""
    if not image_files:
        return False
    
    # Read first image to get dimensions
    first_image = cv2.imread(str(image_files[0]))
    if first_image is None:
        return False
    
    height, width = first_image.shape[:2]
    
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )
    
    if not video_writer.isOpened():
        return False
    
    try:
        for img_path in image_files:
            image = cv2.imread(str(img_path))
            if image is None:
                continue
            video_writer.write(image)
        
        video_writer.release()
        
        # Save hash file to track this timelapse
        hash_file = output_path.parent / f".{output_path.stem}.hash"
        current_hash = get_images_hash(image_files)
        with open(hash_file, 'w') as f:
            f.write(str(current_hash))
        
        return True
        
    except Exception as e:
        return False
    finally:
        video_writer.release()

def process_single_day(args):
    """Process a single day's timelapse. Returns (date, success, message)."""
    workstation, date, date_dir, timelapses_dir = args
    try:
        # Get all PNG files, sorted by name
        png_files = sorted(date_dir.glob("*.png"))
        
        if not png_files:
            return (date, False, f"No PNG files found")
        
        # Create output filename and save in the timelapses folder
        output_filename = f"{workstation}_{date}_timelapse.mp4"
        output_path = timelapses_dir / output_filename
        
        # Check if timelapse needs to be regenerated
        if needs_regeneration(png_files, output_path):
            # Create timelapse
            success = create_timelapse(png_files, output_path, fps=24)
            if success:
                return (date, True, f"Created ({len(png_files)} images)")
            else:
                return (date, False, f"Failed to create")
        else:
            return (date, True, f"Up to date ({len(png_files)} images)")
            
    except Exception as e:
        return (date, False, f"Error: {str(e)[:50]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 simple_timelapse.py <screenshots_path>")
        print("Example: python3 simple_timelapse.py /path/to/screenshots")
        sys.exit(1)
    
    screenshots_path = Path(sys.argv[1])
    if not screenshots_path.exists():
        print(f"Error: Path does not exist: {screenshots_path}")
        sys.exit(1)
    
    print(f"Processing screenshots from: {screenshots_path}")
    print("Saving timelapses to timelapses/ folder under each workstation")
    print()
    
    success_count = 0
    total_count = 0
    
    # Determine number of processes to use
    num_processes = min(mp.cpu_count(), 8)  # Cap at 8 processes to avoid overwhelming the system
    print(f"Using {num_processes} parallel processes")
    print()
    
    # Process each workstation
    for workstation_dir in screenshots_path.iterdir():
        if not workstation_dir.is_dir():
            continue
        
        workstation = workstation_dir.name
        print(f"Processing workstation: {workstation}")
        
        # Create timelapses folder under this workstation
        timelapses_dir = workstation_dir / "timelapses"
        timelapses_dir.mkdir(exist_ok=True)
        
        # Collect all date directories for this workstation
        date_dirs = []
        for date_dir in workstation_dir.iterdir():
            if date_dir.is_dir() and date_dir.name != "timelapses":
                date_dirs.append((date_dir.name, date_dir))
        
        if not date_dirs:
            print(f"  No date directories found for {workstation}")
            continue
        
        total_count += len(date_dirs)
        
        # Process dates in parallel
        with mp.Pool(processes=num_processes) as pool:
            # Prepare arguments for each date
            args = [(workstation, date, date_dir, timelapses_dir) for date, date_dir in date_dirs]
            
            # Process in parallel with progress tracking
            results = []
            for result in tqdm(
                pool.imap_unordered(process_single_day, args),
                total=len(args),
                desc=f"Processing {workstation}",
                unit="day"
            ):
                results.append(result)
        
        # Display results
        print(f"  Results for {workstation}:")
        for date, success, message in sorted(results):
            if success:
                success_count += 1
                print(f"    ✓ {date}: {message}")
            else:
                print(f"    ✗ {date}: {message}")
        print()
    
    print()
    print(f"Complete! Created {success_count}/{total_count} timelapses")
    print("Timelapses saved to timelapses/ folders under each workstation")

if __name__ == "__main__":
    main() 