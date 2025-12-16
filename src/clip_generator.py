"""
Clip generation module for cutting video clips using FFmpeg.
"""

import subprocess
import os


def cut_clip(
    video_path: str,
    start_time: float,
    end_time: float,
    output_path: str,
    clip_index: int
) -> bool:
    """
    Cut a single clip from video using FFmpeg.

    Args:
        video_path: Path to source video
        start_time: Start time in seconds
        end_time: End time in seconds
        output_path: Where to save the clip
        clip_index: Clip number (for progress display)

    Returns:
        True if successful, False otherwise
    """
    duration = end_time - start_time

    # Try fast codec copy first
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', video_path,
        '-t', str(duration),
        '-c', 'copy',  # Fast codec copy
        '-avoid_negative_ts', 'make_zero',  # Fix timestamp issues
        '-y',
        output_path
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, text=True)
        print(f"  ✓ Clip {clip_index} saved")
        return True
    except subprocess.CalledProcessError:
        # Codec copy failed, try re-encoding
        print(f"  ⚠ Codec copy failed for clip {clip_index}, re-encoding...")
        cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', video_path,
            '-t', str(duration),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',
            output_path
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, text=True)
            print(f"  ✓ Clip {clip_index} saved (re-encoded)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to cut clip {clip_index}: {e.stderr}")
            return False


def generate_all_clips(video_path: str, clips: list, output_dir: str) -> list:
    """
    Generate all video clips.

    Args:
        video_path: Path to source video
        clips: List of clip dictionaries with start_time and end_time
        output_dir: Directory where to save clips

    Returns:
        List of successfully generated clip file paths
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    generated_paths = []

    print(f"\n⏳ Cutting {len(clips)} clips with FFmpeg...")

    for i, clip in enumerate(clips, 1):
        output_filename = f"{video_name}_clip_{i:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        success = cut_clip(
            video_path,
            clip['start_time'],
            clip['end_time'],
            output_path,
            i
        )

        if success:
            generated_paths.append(output_path)

    return generated_paths
