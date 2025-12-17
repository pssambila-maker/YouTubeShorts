"""
Report generation module for saving clip suggestions to files.
"""

import json
import os
from datetime import datetime


def generate_json_report(clips: list, video_path: str, output_dir: str) -> str:
    """
    Generate JSON report of clip suggestions.

    Args:
        clips: List of clip dictionaries
        video_path: Path to original video file
        output_dir: Directory where to save the report

    Returns:
        Path to generated JSON file
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{video_name}_clips.json")

    report = {
        "video_path": video_path,
        "video_name": video_name,
        "generated_at": datetime.now().isoformat(),
        "clip_count": len(clips),
        "clips": clips
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return output_path


def format_duration(seconds: float) -> str:
    """
    Convert seconds to MM:SS format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string in MM:SS format
    """
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def generate_text_report(clips: list, video_path: str, output_dir: str) -> str:
    """
    Generate human-readable text report.

    Args:
        clips: List of clip dictionaries
        video_path: Path to original video file
        output_dir: Directory where to save the report

    Returns:
        Path to generated TXT file
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{video_name}_clips.txt")

    lines = [
        "=" * 70,
        "YOUTUBE SHORTS CLIP SUGGESTIONS",
        "=" * 70,
        f"Video: {os.path.basename(video_path)}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Clips: {len(clips)}",
        "=" * 70,
        ""
    ]

    for i, clip in enumerate(clips, 1):
        duration = clip['end_time'] - clip['start_time']
        lines.extend([
            f"CLIP {i}: {clip['title']}",
            f"Time: {format_duration(clip['start_time'])} - {format_duration(clip['end_time'])} ({duration:.0f} seconds)",
            f"",
            f"Hook: {clip.get('hook', clip.get('caption', 'N/A'))}",
            f"Description: {clip.get('description', 'N/A')}",
            f"Thumbnail Text: {clip.get('thumbnail_text', 'N/A')}",
            f"",
            f"Why this works: {clip['reason']}",
            "-" * 70,
            ""
        ])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path
