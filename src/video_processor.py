"""
Video processing module for extracting audio from video files using FFmpeg.
"""

import subprocess
import os


def check_ffmpeg_installed():
    """
    Check if FFmpeg is available on the system.

    Returns:
        bool: True if FFmpeg is installed and accessible, False otherwise
    """
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def extract_audio(video_path: str, output_path: str) -> str:
    """
    Extract audio from video using FFmpeg.

    Args:
        video_path: Path to input video file
        output_path: Path for output audio file (should be .wav)

    Returns:
        Path to extracted audio file

    Raises:
        FileNotFoundError: If video file doesn't exist
        RuntimeError: If FFmpeg is not installed or fails
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not check_ffmpeg_installed():
        raise RuntimeError("FFmpeg is not installed or not in PATH")

    # FFmpeg command: extract audio as WAV, mono, 16kHz (optimized for Whisper)
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # WAV format
        '-ar', '16000',  # 16kHz sample rate
        '-ac', '1',  # Mono
        '-y',  # Overwrite output
        output_path
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, text=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e.stderr}")
