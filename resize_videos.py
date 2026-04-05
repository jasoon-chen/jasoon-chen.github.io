#!/usr/bin/env python3
import subprocess
import os
import glob

# Speed factor (multiply speed by this amount)
speed_factor = 3.5

# Change to videos directory
video_dir = "/Users/jasonchen/Documents/Coding Projects/jasoonchen.com/leonidk.github.io/videos_copy"
os.chdir(video_dir)

# Get all mp4 files
video_files = glob.glob("*.mp4")

for video_file in video_files:
    print(f"\n{'='*60}")
    print(f"Processing: {video_file}")
    print(f"{'='*60}")
    
    # Get duration using ffprobe
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "default=noprint_wrappers=1:nokey=1", video_file],
            capture_output=True,
            text=True
        )
        duration = float(result.stdout.strip())
        print(f"Original duration: {duration:.2f} seconds")
        
        # Calculate new duration
        new_target_duration = duration / speed_factor
        print(f"Speed factor: {speed_factor}x → New duration: {new_target_duration:.2f} seconds")
        
        # Create output filename with suffix
        name, ext = os.path.splitext(video_file)
        output_file = f"{name}_resized{ext}"
        
        # Run ffmpeg with setpts filter and remove audio
        cmd = [
            "ffmpeg",
            "-i", video_file,
            "-vf", f"setpts=PTS/{speed_factor},scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-an",  # Remove audio
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-pix_fmt", "yuv420p",  # Required for web compatibility
            "-movflags", "+faststart",  # Optimize for streaming
            "-y",
            output_file
        ]
        
        print(f"Running ffmpeg to speed up video...")
        result = subprocess.run(cmd, check=True)
        if result.returncode != 0:
            raise Exception(f"ffmpeg failed with return code {result.returncode}")
        
        # Verify new duration
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "default=noprint_wrappers=1:nokey=1", output_file],
            capture_output=True,
            text=True
        )
        new_duration = float(result.stdout.strip())
        print(f"New duration: {new_duration:.2f} seconds")
        print(f"✓ Successfully saved {output_file}")
        
    except Exception as e:
        print(f"✗ Error processing {video_file}: {e}")

print(f"\n{'='*60}")
print("All videos have been resized and saved!")
print("Original videos remain unchanged.")
print(f"{'='*60}")
