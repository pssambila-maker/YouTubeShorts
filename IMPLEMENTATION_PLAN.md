# YouTube Shorts Highlight Extractor - Implementation Plan

## 1. MVP Scope Definition

### WILL DO (Version 1):
- Accept a local video file path as input
- Extract audio from the video using FFmpeg
- Transcribe the audio using OpenAI Whisper (local model)
- Analyze the transcript using Claude API to identify highlight moments
- Generate a report with suggested clips (timestamps, titles, captions)
- Save the report as both JSON and readable text files
- Optionally cut the video into separate clip files using FFmpeg

### WILL NOT DO (Version 1):
- No user authentication or accounts
- No cloud storage or Firebase integration
- No web hosting or online interface
- No batch processing of multiple videos simultaneously
- No advanced video editing (transitions, effects, overlays)
- No direct YouTube upload integration

---

## 2. Tech Stack & Folder Structure

### Tech Stack Choice: **Python**
**Why Python?**
- Easier FFmpeg integration via `ffmpeg-python`
- Better AI/ML library support (Whisper, Claude SDK)
- Simpler file handling and CLI creation
- Easier to read and maintain for an MVP

### Dependencies:
- **Python 3.10+**
- **FFmpeg** (installed on system, called via Python)
- **openai-whisper** - Local speech-to-text transcription
- **anthropic** - Claude API for highlight analysis
- **ffmpeg-python** - Python wrapper for FFmpeg commands
- **python-dotenv** - For API key management

### Folder Structure:
```
YouTubeShorts/
├── .env                          # API keys (ANTHROPIC_API_KEY)
├── .gitignore                    # Ignore .env, output files
├── requirements.txt              # Python dependencies
├── README.md                     # How to use the app
├── main.py                       # CLI entry point
├── config.py                     # Configuration settings
├── src/
│   ├── __init__.py
│   ├── video_processor.py        # Extract audio from video
│   ├── transcriber.py            # Whisper transcription
│   ├── highlight_analyzer.py     # Claude AI highlight detection
│   ├── clip_generator.py         # FFmpeg video cutting
│   └── report_generator.py       # JSON/TXT report creation
├── output/
│   ├── audio/                    # Extracted audio files (temp)
│   ├── transcripts/              # Saved transcripts
│   ├── reports/                  # JSON and TXT clip reports
│   └── clips/                    # Generated video clips (optional)
└── tests/                        # Future: unit tests
    └── test_sample.mp4           # Small test video
```

---

## 3. End-to-End Workflow

### Step-by-Step Process:

**1. User Input**
```bash
python main.py path/to/video.mp4 --max-clips 5
```
- User provides video file path via command-line argument
- Optional flags: `--max-clips`, `--min-duration`, `--max-duration`, `--skip-cutting`

**2. Audio Extraction**
- FFmpeg extracts audio track to `output/audio/video_name_audio.wav`
- WAV format for best Whisper compatibility
- Keeps temp file for debugging, can delete later

**3. Transcription**
- OpenAI Whisper (small or medium model) transcribes the audio
- Generates timestamped transcript with word-level precision
- Saves to `output/transcripts/video_name_transcript.json`
- Format: `[{"start": 0.0, "end": 2.5, "text": "Hello everyone"}, ...]`

**4. Highlight Analysis**
- Sends transcript to Claude API with specialized prompt:
  - "Analyze this transcript and identify 3-5 moments perfect for 15-60 second YouTube Shorts"
  - "Look for: exciting moments, punchlines, key insights, emotional peaks, standalone stories"
  - "For each clip provide: start_time, end_time, title, caption, reason"
- Claude returns structured JSON with clip suggestions
- Uses Claude Sonnet 4.5 for cost-effectiveness

**5. Report Generation**
- Creates `output/reports/video_name_clips.json` (machine-readable)
- Creates `output/reports/video_name_clips.txt` (human-readable)
- Human-readable format:
  ```
  CLIP 1: "Epic Fail Moment"
  Time: 02:15 - 02:42 (27 seconds)
  Caption: "Watch what happens when..."
  Reason: High energy, visual payoff, standalone moment
  ```

**6. Video Cutting (Optional)**
- If `--skip-cutting` is NOT set, FFmpeg cuts each clip
- Saves to `output/clips/video_name_clip_01.mp4`, `_clip_02.mp4`, etc.
- Uses fast codec copy when possible (no re-encoding)
- Preserves original video quality

---

## 4. FFmpeg Integration for Clip Cutting

### Implementation:
- Use `ffmpeg-python` library for Pythonic FFmpeg control
- Command structure for each clip:
  ```python
  ffmpeg.input(video_path, ss=start_time, to=end_time)
        .output(output_path, codec='copy', format='mp4')
        .overwrite_output()
        .run()
  ```

### Key Features:
- `ss` and `to` for precise start/end times
- `codec='copy'` for fast, lossless cutting (no re-encoding)
- Falls back to re-encoding if codec copy fails
- Progress feedback in terminal

### Error Handling:
- Check if FFmpeg is installed at startup
- Validate input video exists and is readable
- Handle FFmpeg errors gracefully with user-friendly messages

---

## 5. User Interface Choice: **Command-Line Interface (CLI)**

### Why CLI for MVP?
- Faster to build (no GUI framework needed)
- More powerful and flexible for power users
- Easier to automate and script
- Can add GUI later if needed

### CLI Commands:
```bash
# Basic usage
python main.py video.mp4

# Advanced usage
python main.py video.mp4 --max-clips 3 --min-duration 15 --max-duration 60

# Skip video cutting, just generate report
python main.py video.mp4 --skip-cutting

# Use larger Whisper model for better accuracy
python main.py video.mp4 --whisper-model medium
```

### CLI Output Example:
```
🎬 YouTube Shorts Clip Extractor
================================

✓ Video loaded: awesome_video.mp4 (15:23 duration)
⏳ Extracting audio... Done (3.2s)
⏳ Transcribing with Whisper (small model)... Done (42.1s)
⏳ Analyzing highlights with Claude AI... Done (8.7s)

Found 4 potential clips:

  1. "Mind-Blowing Revelation" (00:45 - 01:12) - 27s
  2. "Funny Reaction Moment" (03:20 - 03:48) - 28s
  3. "Key Takeaway Summary" (08:15 - 08:55) - 40s
  4. "Epic Conclusion" (14:30 - 15:05) - 35s

⏳ Cutting clips with FFmpeg...
  ✓ Clip 1/4 saved
  ✓ Clip 2/4 saved
  ✓ Clip 3/4 saved
  ✓ Clip 4/4 saved

✅ Complete!
📁 Reports: output/reports/awesome_video_clips.json|.txt
📁 Clips: output/clips/awesome_video_clip_01.mp4 (and 3 more)
```

---

## 6. Module Breakdown

### **main.py** - CLI Entry Point
**Purpose:** Parse arguments, orchestrate the full pipeline
**Functions:**
- `main()` - Entry point, argument parsing with argparse
- `run_pipeline(video_path, options)` - Coordinates all steps
- `check_dependencies()` - Verify FFmpeg and API keys exist

**Inputs:** Command-line arguments
**Outputs:** Exit code (0 = success, 1 = error)

---

### **config.py** - Configuration Settings
**Purpose:** Centralized settings and constants
**Contains:**
- `OUTPUT_DIRS` - Dictionary of output folder paths
- `WHISPER_MODEL` - Default Whisper model ("small")
- `MAX_CLIPS` - Default max clips to generate (5)
- `CLIP_MIN_DURATION` - Minimum clip length (15 seconds)
- `CLIP_MAX_DURATION` - Maximum clip length (60 seconds)
- `load_api_key()` - Load ANTHROPIC_API_KEY from .env

---

### **src/video_processor.py** - Audio Extraction
**Purpose:** Extract audio from video files
**Functions:**
- `extract_audio(video_path: str, output_path: str) -> str`
  - Uses FFmpeg to extract audio as WAV
  - Returns path to audio file
  - Raises exception if FFmpeg fails

**Inputs:** Video file path
**Outputs:** Audio WAV file path

---

### **src/transcriber.py** - Whisper Transcription
**Purpose:** Convert audio to timestamped text
**Functions:**
- `transcribe_audio(audio_path: str, model_name: str = "small") -> dict`
  - Loads Whisper model
  - Transcribes audio with timestamps
  - Returns dict with segments: `{"segments": [{"start": 0, "end": 2.5, "text": "..."}]}`
- `save_transcript(transcript: dict, output_path: str)`
  - Saves transcript as JSON

**Inputs:** Audio file path
**Outputs:** Transcript dictionary with timestamps

---

### **src/highlight_analyzer.py** - Claude AI Analysis
**Purpose:** Use Claude to identify highlight moments
**Functions:**
- `analyze_highlights(transcript: dict, max_clips: int, min_duration: int, max_duration: int) -> list`
  - Builds prompt for Claude with transcript and constraints
  - Calls Claude API (Sonnet 4.5)
  - Parses Claude's response into structured clip objects
  - Returns list of clips: `[{"start": 45.2, "end": 72.1, "title": "...", "caption": "...", "reason": "..."}]`

**Inputs:** Transcript dictionary, clip constraints
**Outputs:** List of clip suggestions with metadata

---

### **src/report_generator.py** - Report Creation
**Purpose:** Save clip suggestions to files
**Functions:**
- `generate_json_report(clips: list, video_path: str, output_dir: str) -> str`
  - Creates JSON file with clip data
  - Returns path to JSON file
- `generate_text_report(clips: list, video_path: str, output_dir: str) -> str`
  - Creates human-readable TXT file
  - Formats clips with headers, timestamps, titles, captions
  - Returns path to TXT file

**Inputs:** Clips list, video path
**Outputs:** Paths to generated report files

---

### **src/clip_generator.py** - FFmpeg Video Cutting
**Purpose:** Cut video into separate clip files
**Functions:**
- `cut_clip(video_path: str, start_time: float, end_time: float, output_path: str, clip_index: int) -> bool`
  - Uses FFmpeg to extract clip from video
  - Tries codec copy first (fast), falls back to re-encode if needed
  - Shows progress in terminal
  - Returns True on success, False on failure
- `generate_all_clips(video_path: str, clips: list, output_dir: str) -> list`
  - Loops through all clips
  - Generates filenames: `video_name_clip_01.mp4`, `_clip_02.mp4`, etc.
  - Returns list of generated file paths

**Inputs:** Video path, clips list
**Outputs:** List of generated clip file paths

---

## 7. Task List for Claude Code

### TASK 1: Project Initialization
**What:** Set up the Python project structure and dependencies
**Files to create:**
- `requirements.txt` with dependencies:
  ```
  openai-whisper
  anthropic
  ffmpeg-python
  python-dotenv
  ```
- `.env.example` template:
  ```
  ANTHROPIC_API_KEY=your_api_key_here
  ```
- `.gitignore` with:
  ```
  .env
  output/
  *.pyc
  __pycache__/
  ```
- `README.md` with basic usage instructions

**Instructions:**
- Initialize the folder structure (src/, output/ subdirectories)
- Create empty `__init__.py` in src/
- Add installation instructions to README

**TODO/Assumptions:**
- User will create their own `.env` file with actual API key
- User will install FFmpeg separately (not via pip)

---

### TASK 2: Configuration Module
**What:** Create centralized configuration
**Files to create:**
- `config.py`

**Functions to implement:**
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Output directories
OUTPUT_DIRS = {
    'audio': 'output/audio',
    'transcripts': 'output/transcripts',
    'reports': 'output/reports',
    'clips': 'output/clips'
}

# Whisper settings
WHISPER_MODEL = 'small'  # Options: tiny, small, medium, large

# Clip constraints
MAX_CLIPS = 5
CLIP_MIN_DURATION = 15  # seconds
CLIP_MAX_DURATION = 60  # seconds

def get_api_key():
    """Load Anthropic API key from environment."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
    return api_key

def create_output_dirs():
    """Create all output directories if they don't exist."""
    for dir_path in OUTPUT_DIRS.values():
        os.makedirs(dir_path, exist_ok=True)
```

**Instructions:**
- Import this config in other modules
- Call `create_output_dirs()` at startup

---

### TASK 3: Video Processor Module
**What:** Implement audio extraction with FFmpeg
**Files to create:**
- `src/video_processor.py`

**Functions to implement:**
```python
import subprocess
import os

def check_ffmpeg_installed():
    """Check if FFmpeg is available on the system."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
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
        RuntimeError: If FFmpeg fails
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not check_ffmpeg_installed():
        raise RuntimeError("FFmpeg is not installed or not in PATH")

    # FFmpeg command: extract audio as WAV, mono, 16kHz (good for Whisper)
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
```

**Inputs:** Video file path
**Outputs:** Audio WAV file

**TODO:**
- Later add progress bar for long videos

---

### TASK 4: Transcriber Module
**What:** Implement Whisper transcription
**Files to create:**
- `src/transcriber.py`

**Functions to implement:**
```python
import whisper
import json
import os

def transcribe_audio(audio_path: str, model_name: str = "small") -> dict:
    """
    Transcribe audio using OpenAI Whisper.

    Args:
        audio_path: Path to audio file
        model_name: Whisper model size (tiny, small, medium, large)

    Returns:
        Dict with 'segments' containing timestamped text:
        {
            "text": "full transcript",
            "segments": [
                {"start": 0.0, "end": 2.5, "text": "Hello"},
                ...
            ]
        }
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print("Transcribing audio...")
    result = model.transcribe(audio_path, verbose=False)

    return result

def save_transcript(transcript: dict, output_path: str):
    """Save transcript to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)
```

**Inputs:** Audio file path
**Outputs:** Transcript dictionary with timestamps

**TODO:**
- First run will download Whisper model (takes time, note this in README)
- Could add option to use faster Whisper models for quicker processing

---

### TASK 5: Highlight Analyzer Module
**What:** Use Claude API to identify clips
**Files to create:**
- `src/highlight_analyzer.py`

**Functions to implement:**
```python
import anthropic
from config import get_api_key

def build_analysis_prompt(transcript: dict, max_clips: int, min_duration: int, max_duration: int) -> str:
    """Build the prompt for Claude."""
    full_text = transcript.get('text', '')
    segments = transcript.get('segments', [])

    # Format segments with timestamps
    formatted_segments = []
    for seg in segments:
        formatted_segments.append(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")

    segments_text = "\n".join(formatted_segments)

    prompt = f"""You are an expert YouTube Shorts creator. Analyze this video transcript and identify the {max_clips} BEST moments to turn into viral YouTube Shorts (15-60 second clips).

TRANSCRIPT:
{segments_text}

CRITERIA FOR GREAT SHORTS:
- Self-contained stories or moments (make sense without context)
- High energy, emotional peaks, or funny moments
- Clear punchlines, revelations, or key insights
- Visual moments that would be compelling
- Duration between {min_duration} and {max_duration} seconds

For each suggested clip, provide:
1. start_time (in seconds, from the timestamps above)
2. end_time (in seconds)
3. title (catchy, 5-8 words)
4. caption (engaging hook for the clip, 10-20 words)
5. reason (why this moment works as a Short)

Return your response as a JSON array ONLY (no other text):
[
  {{
    "start_time": 45.2,
    "end_time": 72.1,
    "title": "Epic Fail Moment",
    "caption": "You won't believe what happens next when he tries this trick!",
    "reason": "High energy moment with visual payoff and standalone story"
  }}
]"""

    return prompt

def analyze_highlights(transcript: dict, max_clips: int = 5, min_duration: int = 15, max_duration: int = 60) -> list:
    """
    Use Claude API to analyze transcript and find highlights.

    Args:
        transcript: Whisper transcript dict
        max_clips: Maximum number of clips to suggest
        min_duration: Minimum clip length in seconds
        max_duration: Maximum clip length in seconds

    Returns:
        List of clip dicts with start_time, end_time, title, caption, reason
    """
    client = anthropic.Anthropic(api_key=get_api_key())

    prompt = build_analysis_prompt(transcript, max_clips, min_duration, max_duration)

    print("Analyzing highlights with Claude AI...")
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Parse Claude's response
    response_text = message.content[0].text

    # Extract JSON from response (Claude might add markdown code blocks)
    import json
    import re

    # Try to find JSON in the response
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if json_match:
        clips = json.loads(json_match.group(0))
    else:
        clips = json.loads(response_text)

    return clips
```

**Inputs:** Transcript, clip parameters
**Outputs:** List of clip suggestions

**TODO:**
- Add error handling for API failures
- Could add retry logic for rate limits
- Might need to adjust prompt based on results

---

### TASK 6: Report Generator Module
**What:** Save clip suggestions to JSON and text files
**Files to create:**
- `src/report_generator.py`

**Functions to implement:**
```python
import json
import os
from datetime import datetime

def generate_json_report(clips: list, video_path: str, output_dir: str) -> str:
    """
    Generate JSON report of clip suggestions.

    Returns:
        Path to generated JSON file
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{video_name}_clips.json")

    report = {
        "video_path": video_path,
        "generated_at": datetime.now().isoformat(),
        "clip_count": len(clips),
        "clips": clips
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return output_path

def format_duration(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def generate_text_report(clips: list, video_path: str, output_dir: str) -> str:
    """
    Generate human-readable text report.

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
            f"Caption: {clip['caption']}",
            f"Reason: {clip['reason']}",
            "-" * 70,
            ""
        ])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path
```

**Inputs:** Clips list, video path
**Outputs:** Paths to JSON and TXT files

---

### TASK 7: Clip Generator Module
**What:** Cut video clips using FFmpeg
**Files to create:**
- `src/clip_generator.py`

**Functions to implement:**
```python
import subprocess
import os

def cut_clip(video_path: str, start_time: float, end_time: float, output_path: str, clip_index: int) -> bool:
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
```

**Inputs:** Video path, clips list
**Outputs:** List of generated clip files

**TODO:**
- Could add progress bars for long clips
- Could add option to add subtitles/captions to clips

---

### TASK 8: Main CLI Entry Point
**What:** Create the main program that ties everything together
**Files to create:**
- `main.py`

**Functions to implement:**
```python
import argparse
import os
import sys
from config import get_api_key, create_output_dirs, OUTPUT_DIRS, WHISPER_MODEL, MAX_CLIPS, CLIP_MIN_DURATION, CLIP_MAX_DURATION
from src.video_processor import extract_audio, check_ffmpeg_installed
from src.transcriber import transcribe_audio, save_transcript
from src.highlight_analyzer import analyze_highlights
from src.report_generator import generate_json_report, generate_text_report
from src.clip_generator import generate_all_clips

def check_dependencies():
    """Verify all required dependencies are available."""
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
        print("\nPlease install FFmpeg and create a .env file with ANTHROPIC_API_KEY")
        sys.exit(1)

def run_pipeline(video_path: str, args):
    """Execute the full highlight extraction pipeline."""

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
    transcript = transcribe_audio(audio_path, args.whisper_model)
    transcript_path = os.path.join(OUTPUT_DIRS['transcripts'], f"{video_name}_transcript.json")
    save_transcript(transcript, transcript_path)
    print("✓ Transcription complete")

    # Step 3: Analyze highlights
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
        print(f"\n  {i}. \"{clip['title']}\"")
        print(f"     Time: {clip['start_time']:.1f}s - {clip['end_time']:.1f}s ({duration:.0f}s)")
        print(f"     {clip['caption']}")

    # Step 4: Generate reports
    print("\n⏳ Generating reports...")
    json_path = generate_json_report(clips, video_path, OUTPUT_DIRS['reports'])
    txt_path = generate_text_report(clips, video_path, OUTPUT_DIRS['reports'])
    print(f"✓ Reports saved:")
    print(f"  - {json_path}")
    print(f"  - {txt_path}")

    # Step 5: Cut clips (optional)
    if not args.skip_cutting:
        clip_paths = generate_all_clips(video_path, clips, OUTPUT_DIRS['clips'])
        print(f"\n✓ {len(clip_paths)} clips saved to {OUTPUT_DIRS['clips']}/")
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
  python main.py video.mp4
  python main.py video.mp4 --max-clips 3 --skip-cutting
  python main.py video.mp4 --whisper-model medium --max-duration 45
        """
    )

    parser.add_argument(
        'video_path',
        help='Path to the video file to process'
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
        help=f'Whisper model size (default: {WHISPER_MODEL})'
    )

    parser.add_argument(
        '--skip-cutting',
        action='store_true',
        help='Skip video cutting, only generate reports'
    )

    args = parser.parse_args()

    # Setup
    create_output_dirs()
    check_dependencies()

    # Run pipeline
    try:
        run_pipeline(args.video_path, args)
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
```

**Inputs:** Command-line arguments
**Outputs:** Exit code, console output

---

### TASK 9: README Documentation
**What:** Create user-friendly documentation
**Files to create:**
- `README.md`

**Content to include:**
```markdown
# YouTube Shorts Highlight Extractor

Automatically find and extract the best moments from long videos to create YouTube Shorts.

## What It Does

1. Analyzes your long-form videos using AI
2. Identifies 3-5 highlight moments perfect for YouTube Shorts
3. Generates reports with timestamps, titles, and captions
4. Optionally cuts the video into separate clip files

## Requirements

- Python 3.10 or higher
- FFmpeg (installed on your system)
- Anthropic API key (Claude)

## Installation

[Include step-by-step setup instructions]

## Usage

[Include examples and command-line options]

## Cost Estimate

- Whisper: Free (runs locally)
- Claude API: ~$0.01-0.05 per video (varies by length)
- FFmpeg: Free

## Troubleshooting

[Common issues and solutions]
```

---

### TASK 10: Testing & Validation
**What:** Test the complete pipeline
**Steps:**
1. Find a small test video (2-3 minutes)
2. Run the full pipeline: `python main.py test_video.mp4`
3. Verify all outputs are created correctly
4. Check clip quality and timestamps
5. Test edge cases (very short video, very long video, video with no speech)

**Files to test:**
- Audio extraction quality
- Transcript accuracy
- Claude's clip suggestions (are they good?)
- FFmpeg clip cutting (correct timestamps?)

**TODO:**
- Add unit tests for each module
- Add integration tests
- Create sample videos for testing

---

## 8. Additional Notes & Future Enhancements

### Assumptions:
- User has a valid Anthropic API key
- User will manually upload clips to YouTube (no auto-upload)
- Videos are in standard formats (MP4, MOV, AVI, etc.)
- Audio track exists and is in a language Whisper supports

### Potential Future Features:
- Batch processing of multiple videos
- Web GUI with drag-and-drop
- Auto-generate thumbnails for each clip
- Add subtitles/captions to video clips
- YouTube upload integration
- Support for multiple languages
- Custom AI prompts for different content types
- Video preview before cutting

### Cost Considerations:
- Whisper: Free (runs locally, but uses CPU/GPU)
- Claude API: ~$0.01-0.05 per 10-minute video (Sonnet 4.5 pricing)
- FFmpeg: Free
- Total cost per video: Under $0.10 typically

---

## Quick Start Checklist

- [ ] Install Python 3.10+
- [ ] Install FFmpeg
- [ ] Clone/create project folder
- [ ] Create `.env` file with `ANTHROPIC_API_KEY=your_key`
- [ ] Run `pip install -r requirements.txt`
- [ ] Test with: `python main.py path/to/test_video.mp4`
- [ ] Check `output/` folders for results
- [ ] Upload clips to YouTube manually

---

**This plan is ready to hand to Claude Code for step-by-step implementation!**
