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
    clip_index: int,
    vertical: bool = False
) -> bool:
    """
    Cut a single clip from video using FFmpeg.

    Args:
        video_path: Path to source video
        start_time: Start time in seconds
        end_time: End time in seconds
        output_path: Where to save the clip
        clip_index: Clip number (for progress display)
        vertical: If True, convert to 9:16 vertical format with blur bars

    Returns:
        True if successful, False otherwise
    """
    duration = end_time - start_time

    if vertical:
        # Convert to vertical 9:16 format (1080x1920) with blurred background
        # This creates the Instagram/TikTok style with blur bars
        cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', video_path,
            '-t', str(duration),
            '-filter_complex',
            '[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black[main];'
            '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,boxblur=luma_radius=min(h\\,w)/20:luma_power=1:chroma_radius=min(cw\\,ch)/20:chroma_power=1[bg];'
            '[bg][main]overlay=(W-w)/2:(H-h)/2',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '48000',  # 48kHz sample rate (standard for video)
            '-ac', '2',  # Stereo audio
            '-movflags', '+faststart',  # Enable streaming/web playback
            '-y',
            output_path
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, text=True)
            print(f"  ✓ Clip {clip_index} saved (vertical 9:16)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to create vertical clip {clip_index}: {e.stderr}")
            return False
    else:
        # Original horizontal clip (fast codec copy)
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
                '-b:a', '128k',
                '-ar', '48000',  # 48kHz sample rate
                '-ac', '2',  # Stereo audio
                '-movflags', '+faststart',  # Enable web playback
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


def generate_all_clips(video_path: str, clips: list, output_dir: str, vertical: bool = False) -> list:
    """
    Generate all video clips.

    Args:
        video_path: Path to source video
        clips: List of clip dictionaries with start_time and end_time
        output_dir: Directory where to save clips
        vertical: If True, convert clips to 9:16 vertical format

    Returns:
        List of successfully generated clip file paths
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    generated_paths = []

    format_msg = "vertical 9:16" if vertical else "original format"
    print(f"\n⏳ Cutting {len(clips)} clips with FFmpeg ({format_msg})...")

    for i, clip in enumerate(clips, 1):
        output_filename = f"{video_name}_clip_{i:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        success = cut_clip(
            video_path,
            clip['start_time'],
            clip['end_time'],
            output_path,
            i,
            vertical=vertical
        )

        if success:
            generated_paths.append(output_path)

    return generated_paths
