# YouTube Shorts Highlight Extractor

Automatically find and extract the best moments from long videos to create YouTube Shorts using AI.

## What It Does

1. **Analyzes** your long-form videos using AI (Whisper + Claude)
2. **Identifies** 3-5 highlight moments perfect for YouTube Shorts (15-60 seconds)
3. **Generates** reports with timestamps, titles, and captions
4. **Optionally cuts** the video into separate clip files ready to upload

## Requirements

- **Python 3.10 or higher**
- **FFmpeg** (installed on your system)
- **Anthropic API key** (for Claude AI)

## Installation

### 1. Install Python
Make sure you have Python 3.10+ installed:
```bash
python --version
```

### 2. Install FFmpeg

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to PATH environment variable

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### 3. Clone/Download This Project
```bash
cd d:\YouTubeShorts
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First run will download the Whisper model (~150MB for 'small' model). This is normal and only happens once.

### 5. Set Up API Key
1. Get your Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
2. Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

## Usage

### Basic Usage
```bash
python main.py path/to/your/video.mp4
```

### Advanced Options
```bash
# Generate only 3 clips
python main.py video.mp4 --max-clips 3

# Use larger Whisper model for better accuracy
python main.py video.mp4 --whisper-model medium

# Only generate reports, don't cut video files
python main.py video.mp4 --skip-cutting

# Custom clip duration constraints
python main.py video.mp4 --min-duration 20 --max-duration 45

# Combine options
python main.py video.mp4 --max-clips 3 --whisper-model medium --max-duration 50
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-clips` | Maximum number of clips to generate | 5 |
| `--min-duration` | Minimum clip length in seconds | 15 |
| `--max-duration` | Maximum clip length in seconds | 60 |
| `--whisper-model` | Whisper model size: tiny, small, medium, large | small |
| `--skip-cutting` | Only generate reports, don't cut videos | False |

## Output

After processing, you'll find:

```
output/
├── audio/
│   └── your_video_audio.wav          # Extracted audio (temp)
├── transcripts/
│   └── your_video_transcript.json    # Full timestamped transcript
├── reports/
│   ├── your_video_clips.json         # Machine-readable clip data
│   └── your_video_clips.txt          # Human-readable clip report
└── clips/
    ├── your_video_clip_01.mp4        # First suggested clip
    ├── your_video_clip_02.mp4        # Second suggested clip
    └── ...
```

### Example Output
```
🎬 YouTube Shorts Clip Extractor
==================================================

✓ Video loaded: awesome_podcast.mp4

⏳ Extracting audio...
✓ Audio extraction complete

⏳ Transcribing with Whisper (small model)...
✓ Transcription complete

⏳ Analyzing highlights with Claude AI...
✓ Found 4 potential clips

==================================================
SUGGESTED CLIPS:
==================================================

  1. "Mind-Blowing Revelation"
     Time: 45.2s - 72.1s (27s)
     You won't believe what happens when he explains this concept!

  2. "Hilarious Story"
     Time: 203.5s - 231.8s (28s)
     The funniest moment from the entire conversation!

  3. "Key Takeaway"
     Time: 512.3s - 552.7s (40s)
     This one insight will change how you think about productivity!

  4. "Epic Conclusion"
     Time: 890.1s - 925.4s (35s)
     The perfect ending that ties everything together!

⏳ Generating reports...
✓ Reports saved

⏳ Cutting 4 clips with FFmpeg...
  ✓ Clip 1/4 saved
  ✓ Clip 2/4 saved
  ✓ Clip 3/4 saved
  ✓ Clip 4/4 saved

✅ Complete!
```

## Cost Estimate

- **Whisper**: Free (runs locally on your computer)
- **Claude API**: ~$0.01-0.05 per video (varies by length)
- **FFmpeg**: Free
- **Total**: Under $0.10 per video typically

## Troubleshooting

### "FFmpeg is not installed or not in PATH"
- Make sure FFmpeg is installed and accessible from command line
- Try running `ffmpeg -version` to verify

### "ANTHROPIC_API_KEY not found in .env file"
- Make sure you created a `.env` file (not `.env.example`)
- Check that your API key is valid
- Restart your terminal after creating the file

### Whisper model download is slow
- First run downloads the model (~150MB for small, ~1.5GB for medium)
- Use `--whisper-model tiny` for faster downloads (less accurate)
- Downloaded models are cached for future use

### Clips are cut at wrong timestamps
- Try re-encoding instead of codec copy (automatic fallback)
- Check the transcript JSON to verify Whisper accuracy
- Use a larger Whisper model for better timestamp precision

### Out of memory errors
- Use a smaller Whisper model (`--whisper-model tiny`)
- Process shorter videos
- Close other applications

## Tips for Best Results

1. **Video Quality**: Use videos with clear audio (minimal background noise)
2. **Content Type**: Works best with:
   - Podcasts and interviews
   - Tutorial videos
   - Vlogs with storytelling
   - Commentary and reactions
3. **Video Length**: 5-30 minutes is ideal (too short = few clips, too long = slower processing)
4. **Review Suggestions**: Always review the text report before uploading clips
5. **Customize Clips**: Edit the generated clips.json to adjust timestamps before cutting

## Project Structure

```
YouTubeShorts/
├── main.py                    # CLI entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .env                       # API keys (create this)
├── src/
│   ├── video_processor.py     # FFmpeg audio extraction
│   ├── transcriber.py         # Whisper transcription
│   ├── highlight_analyzer.py  # Claude AI analysis
│   ├── report_generator.py    # JSON/TXT report creation
│   └── clip_generator.py      # FFmpeg video cutting
└── output/                    # All generated files
```

## Future Enhancements

Planned features for future versions:
- Batch processing of multiple videos
- Web GUI with drag-and-drop
- Auto-generate thumbnails
- Add subtitles to clips
- YouTube upload integration
- Custom AI prompts per content type

## License

MIT License - Use freely for personal or commercial projects.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the IMPLEMENTATION_PLAN.md for technical details
3. Open an issue on GitHub (if applicable)

---

**Happy clip creating!** 🎬✨
