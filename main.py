"""
YouTube Shorts Highlight Extractor - Main CLI Entry Point

This tool analyzes long-form videos and identifies the best moments
for creating YouTube Shorts using AI (Whisper + Claude).
"""

import argparse
import os
import sys
import tkinter as tk
from tkinter import filedialog
from config import (
    get_api_key,
    create_output_dirs,
    OUTPUT_DIRS,
    WHISPER_MODEL,
    MAX_CLIPS,
    CLIP_MIN_DURATION,
    CLIP_MAX_DURATION
)
from src.video_processor import extract_audio, check_ffmpeg_installed
from src.transcriber import transcribe_audio, save_transcript
from src.highlight_analyzer import analyze_highlights
from src.report_generator import generate_json_report, generate_text_report
from src.clip_generator import generate_all_clips
from src.video_metadata_generator import generate_video_metadata


def check_dependencies():
    """
    Verify all required dependencies are available.

    Exits the program if dependencies are missing.
    """
    errors = []

    # Check FFmpeg
    if not check_ffmpeg_installed():
        errors.append("FFmpeg is not installed or not in PATH")

    # Check API key
    try:
        get_api_key()
    except ValueError as e:
        errors.append(str(e))

    if errors:
        print("❌ Missing dependencies:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease:")
        print("  1. Install FFmpeg: https://ffmpeg.org/download.html")
        print("  2. Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)


def select_video_file():
    """
    Open a GUI file picker to select a video file.

    Returns:
        str: Path to selected video file, or None if cancelled
    """
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[
            ("Video files", "*.mp4 *.mov *.avi *.mkv *.flv *.wmv *.webm"),
            ("MP4 files", "*.mp4"),
            ("All files", "*.*")
        ]
    )

    root.destroy()
    return file_path if file_path else None


def run_pipeline(video_path: str, args):
    """
    Execute the full highlight extraction pipeline.

    Args:
        video_path: Path to the video file to process
        args: Parsed command-line arguments
    """

    print("\n🎬 YouTube Shorts Clip Extractor")
    print("=" * 50)

    # Validate video file
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        sys.exit(1)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"\n✓ Video loaded: {os.path.basename(video_path)}")

    # Step 1: Extract audio
    print("\n⏳ Extracting audio...")
    audio_path = os.path.join(OUTPUT_DIRS['audio'], f"{video_name}_audio.wav")
    extract_audio(video_path, audio_path)
    print("✓ Audio extraction complete")

    # Step 2: Transcribe
    print(f"\n⏳ Transcribing with Whisper ({args.whisper_model} model)...")
    print("   (First run will download the model, this may take a few minutes)")
    transcript = transcribe_audio(audio_path, args.whisper_model)
    transcript_path = os.path.join(OUTPUT_DIRS['transcripts'], f"{video_name}_transcript.json")
    save_transcript(transcript, transcript_path)
    print("✓ Transcription complete")

    # Step 3A: Generate full video metadata
    print(f"\n⏳ Generating full video metadata with Claude AI...")
    video_metadata = generate_video_metadata(transcript, video_name)
    print(f"✓ Video metadata generated")
    print(f"   Title: {video_metadata['title']}")
    print(f"   Category: {video_metadata['category']}")

    # Step 3B: Analyze highlights
    print(f"\n⏳ Analyzing highlights with Claude AI...")
    clips = analyze_highlights(
        transcript,
        max_clips=args.max_clips,
        min_duration=args.min_duration,
        max_duration=args.max_duration
    )
    print(f"✓ Found {len(clips)} potential clips")

    # Display clips
    print("\n" + "=" * 50)
    print("SUGGESTED CLIPS:")
    print("=" * 50)
    for i, clip in enumerate(clips, 1):
        duration = clip['end_time'] - clip['start_time']
        start_min = int(clip['start_time'] // 60)
        start_sec = int(clip['start_time'] % 60)
        end_min = int(clip['end_time'] // 60)
        end_sec = int(clip['end_time'] % 60)
        print(f"\n  {i}. \"{clip['title']}\"")
        print(f"     Time: {start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d} ({duration:.0f}s)")
        print(f"     Hook: {clip.get('hook', clip.get('caption', 'N/A'))}")
        print(f"     Thumbnail: {clip.get('thumbnail_text', 'N/A')}")

    # Step 4: Generate reports
    print("\n⏳ Generating reports...")

    # Save video metadata
    import json as json_module
    metadata_json_path = os.path.join(OUTPUT_DIRS['reports'], f"{video_name}_metadata.json")
    with open(metadata_json_path, 'w', encoding='utf-8') as f:
        json_module.dump(video_metadata, f, indent=2, ensure_ascii=False)

    # Create human-readable metadata report
    metadata_txt_path = os.path.join(OUTPUT_DIRS['reports'], f"{video_name}_metadata.txt")
    with open(metadata_txt_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("FULL VIDEO YOUTUBE METADATA\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"TITLE:\n{video_metadata['title']}\n\n")
        f.write(f"DESCRIPTION:\n{video_metadata['description']}\n\n")
        f.write(f"TAGS:\n{', '.join(video_metadata['tags'])}\n\n")
        f.write(f"THUMBNAIL TEXT:\n{video_metadata['thumbnail_text']}\n\n")
        f.write(f"CATEGORY:\n{video_metadata['category']}\n\n")
        f.write("KEY MOMENTS / CHAPTERS:\n")
        for moment in video_metadata.get('key_moments', []):
            f.write(f"  {moment['timestamp']} - {moment['description']}\n")
        f.write("\n" + "=" * 70 + "\n")

    # Save clips reports
    json_path = generate_json_report(clips, video_path, OUTPUT_DIRS['reports'])
    txt_path = generate_text_report(clips, video_path, OUTPUT_DIRS['reports'])

    print(f"✓ Reports saved:")
    print(f"  Full Video Metadata:")
    print(f"    - {metadata_json_path}")
    print(f"    - {metadata_txt_path}")
    print(f"  Clips Reports:")
    print(f"    - {json_path}")
    print(f"    - {txt_path}")

    # Step 5: Cut clips (optional)
    if not args.skip_cutting:
        clip_paths = generate_all_clips(video_path, clips, OUTPUT_DIRS['clips'], vertical=args.vertical)
        format_info = " (vertical 9:16)" if args.vertical else ""
        print(f"\n✓ {len(clip_paths)} clips saved to {OUTPUT_DIRS['clips']}/{format_info}")
    else:
        print("\n⏭  Skipped video cutting (--skip-cutting flag)")

    print("\n✅ Complete!\n")


def main():
    """Main entry point with argument parsing."""

    parser = argparse.ArgumentParser(
        description="Extract highlight clips from long videos for YouTube Shorts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                      (opens GUI file picker)
  python main.py video.mp4
  python main.py video.mp4 --vertical (creates vertical 9:16 clips for phones)
  python main.py video.mp4 --max-clips 3 --skip-cutting
  python main.py video.mp4 --whisper-model medium --max-duration 45 --vertical
  python main.py "path/with spaces/video.mp4" --max-clips 5

For more information, see README.md
        """
    )

    parser.add_argument(
        'video_path',
        nargs='?',  # Make video_path optional
        help='Path to the video file to process (or leave empty to use GUI file picker)'
    )

    parser.add_argument(
        '--max-clips',
        type=int,
        default=MAX_CLIPS,
        help=f'Maximum number of clips to generate (default: {MAX_CLIPS})'
    )

    parser.add_argument(
        '--min-duration',
        type=int,
        default=CLIP_MIN_DURATION,
        help=f'Minimum clip duration in seconds (default: {CLIP_MIN_DURATION})'
    )

    parser.add_argument(
        '--max-duration',
        type=int,
        default=CLIP_MAX_DURATION,
        help=f'Maximum clip duration in seconds (default: {CLIP_MAX_DURATION})'
    )

    parser.add_argument(
        '--whisper-model',
        choices=['tiny', 'small', 'medium', 'large'],
        default=WHISPER_MODEL,
        help=f'Whisper model size (default: {WHISPER_MODEL}). Larger = more accurate but slower'
    )

    parser.add_argument(
        '--skip-cutting',
        action='store_true',
        help='Skip video cutting, only generate reports'
    )

    parser.add_argument(
        '--vertical',
        action='store_true',
        help='Convert clips to vertical 9:16 format (1080x1920) with blurred background for phone screens'
    )

    args = parser.parse_args()

    # Setup
    create_output_dirs()
    check_dependencies()

    # Get video path - use GUI file picker if not provided
    video_path = args.video_path
    if not video_path:
        print("No video path provided. Opening file picker...")
        video_path = select_video_file()
        if not video_path:
            print("❌ No file selected. Exiting.")
            sys.exit(1)
        print(f"Selected: {video_path}\n")

    # Run pipeline
    try:
        run_pipeline(video_path, args)
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
