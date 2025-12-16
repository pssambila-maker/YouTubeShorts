# Quick Start Guide

## Setup (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `openai-whisper` - AI transcription (first run downloads ~150MB model)
- `anthropic` - Claude API client
- `ffmpeg-python` - Video processing wrapper
- `python-dotenv` - Environment variable management

### 2. Install FFmpeg

**Already installed?** Check with:
```bash
ffmpeg -version
```

**Not installed?**
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### 3. Get Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Create an API key
4. Copy the key

### 4. Create .env File

Create a file named `.env` (no extension) in the project root:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

**Important:** This is `.env`, NOT `.env.example`

## Test Run

Use a short video (2-5 minutes) for your first test:

```bash
python main.py path/to/test_video.mp4
```

The app will:
1. Extract audio (a few seconds)
2. Download Whisper model on first run (one-time, 2-3 minutes)
3. Transcribe the audio (20-60 seconds)
4. Analyze with Claude (5-10 seconds)
5. Generate reports and cut clips (10-30 seconds)

## Expected Output

```
output/
├── audio/test_video_audio.wav
├── transcripts/test_video_transcript.json
├── reports/
│   ├── test_video_clips.json
│   └── test_video_clips.txt
└── clips/
    ├── test_video_clip_01.mp4
    ├── test_video_clip_02.mp4
    └── ...
```

## Troubleshooting

### "FFmpeg is not installed"
- Run `ffmpeg -version` to verify installation
- Make sure FFmpeg is in your system PATH
- Restart your terminal after installing

### "ANTHROPIC_API_KEY not found"
- Verify `.env` file exists (not `.env.example`)
- Check there are no spaces around the `=` sign
- Make sure the API key starts with `sk-ant-`

### Whisper model download fails
- Check your internet connection
- Try a smaller model: `--whisper-model tiny`
- Models are cached in `~/.cache/whisper/`

### Out of memory
- Use smaller Whisper model: `--whisper-model tiny`
- Process shorter videos
- Close other applications

## Next Steps

Once your test run succeeds:

1. **Review the output** in `output/reports/` to see suggested clips
2. **Try different options**: `python main.py video.mp4 --help`
3. **Process your actual videos**: Point to your long-form content
4. **Upload to YouTube**: Use the clips in `output/clips/`

## Cost Estimate

- Whisper: Free (runs locally)
- Claude API: ~$0.01-0.05 per 10-minute video
- FFmpeg: Free

**Total: Under $0.10 per video**

## Command Examples

```bash
# Basic usage
python main.py my_video.mp4

# Only 3 clips, skip cutting
python main.py my_video.mp4 --max-clips 3 --skip-cutting

# Better accuracy, shorter clips
python main.py my_video.mp4 --whisper-model medium --max-duration 45

# Quick test (tiny model, just reports)
python main.py my_video.mp4 --whisper-model tiny --skip-cutting
```

---

**You're ready to go!** 🚀

For detailed documentation, see [README.md](README.md)
