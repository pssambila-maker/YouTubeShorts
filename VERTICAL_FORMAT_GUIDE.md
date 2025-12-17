# Vertical Format Guide (9:16 for Phone Screens)

## Overview

The `--vertical` flag automatically converts your horizontal videos into vertical 9:16 format optimized for mobile viewing on YouTube Shorts, TikTok, Instagram Reels, and Facebook Reels.

## How It Works

### Visual Transformation

```
BEFORE (Horizontal 16:9)          AFTER (Vertical 9:16)
┌─────────────────────┐          ┌─────────┐
│                     │          │ ░░░░░░░ │ ← Blurred background
│                     │          │ ┌─────┐ │
│    Your Video       │    →     │ │Video│ │ ← Original video
│                     │          │ └─────┘ │
│                     │          │ ░░░░░░░ │ ← Blurred background
└─────────────────────┘          └─────────┘
  1920x1080 (16:9)                1080x1920 (9:16)
```

### Technical Details

- **Output Resolution**: 1080x1920 pixels (9:16 aspect ratio)
- **Original Video**: Centered and scaled to fit
- **Background**: Blurred and zoomed version of your video
- **Quality**: High quality (CRF 23, fast preset)
- **Audio**: AAC 128kbps (preserved from original)

## Usage Examples

### Basic Vertical Conversion
```bash
python main.py video.mp4 --vertical
```

### Music Video (Recommended Settings)
```bash
python main.py music_video.mp4 --vertical --max-clips 3 --max-duration 30
```

### High Quality with Better Whisper
```bash
python main.py video.mp4 --vertical --whisper-model medium --max-clips 5
```

### Just Preview (No Cutting)
```bash
python main.py video.mp4 --vertical --skip-cutting
```
This generates reports showing what clips would be created without actually cutting them.

## When to Use Vertical Format

### ✅ Best For:

**Music Videos**
- Keeps full performance visible
- Blurred background adds professional look
- Perfect for chorus/hook moments
- No important visual elements get cropped

**Landscape Content**
- Wide-angle shots
- Action across the frame
- Scenic videos
- Content where context matters

**Product Reviews**
- Shows full product and surroundings
- Professional presentation
- Nothing gets cut off

### ⚠️ Consider Alternatives For:

**Already Vertical Content**
- If your source is 9:16, use without `--vertical`
- Portrait phone videos don't need conversion

**Talking Head / Centered Subjects**
- Could use center crop instead (future feature)
- Vertical conversion still works, just adds blur bars

## Comparison: Vertical vs Horizontal

| Aspect | Horizontal (Default) | Vertical (--vertical) |
|--------|---------------------|----------------------|
| Resolution | Same as source | 1080x1920 |
| Aspect Ratio | Same as source | 9:16 |
| Processing Time | ~5-10s per clip | ~20-30s per clip |
| File Size | Smaller | Slightly larger |
| Best For | Desktop viewing | Mobile viewing |
| YouTube Shorts | Works | Optimized ✓ |
| TikTok | Works | Optimized ✓ |
| Instagram Reels | Works | Optimized ✓ |

## Processing Time

Vertical conversion is slower because it re-encodes the video with filters:

- **Horizontal clip**: 5-10 seconds (codec copy)
- **Vertical clip**: 20-30 seconds (re-encoding + blur effect)

For a 5-clip video:
- Horizontal: ~30-60 seconds total
- Vertical: ~2-3 minutes total

## Quality Settings

The vertical conversion uses:

```
Codec: H.264 (libx264)
Preset: fast (good balance of speed/quality)
CRF: 23 (high quality, small file size)
Audio: AAC 128kbps
```

### Want Higher Quality?

You can manually edit `src/clip_generator.py` and change:
- `'-crf', '23'` to `'-crf', '18'` (better quality, larger files)
- `'-preset', 'fast'` to `'-preset', 'slow'` (better quality, slower)

## Troubleshooting

### Clips are too slow to generate
**Solution**: Processing 9:16 video requires re-encoding. For faster results:
- Use `--skip-cutting` to just get the report first
- Review suggested clips before cutting
- Only cut the clips you actually want

### Blur looks pixelated
**Solution**: This happens with low-resolution source videos
- Use at least 720p source video
- Higher source resolution = better blur quality

### Original video looks stretched
**Solution**: This shouldn't happen with the current implementation
- Check your source video isn't already corrupted
- Try without `--vertical` to verify source quality

### Black bars instead of blur
**Solution**: The filter might have failed
- Check the console for FFmpeg errors
- Verify FFmpeg version is up to date: `ffmpeg -version`

## File Naming

Vertical clips use the same naming as horizontal:
```
your_video_clip_01.mp4
your_video_clip_02.mp4
your_video_clip_03.mp4
```

The format is encoded in the video itself, not the filename.

## Platform Optimization

### YouTube Shorts
- ✅ 9:16 format preferred
- ✅ Up to 60 seconds
- ✅ 1080x1920 recommended

### TikTok
- ✅ 9:16 format required
- ✅ Up to 10 minutes (but shorter is better)
- ✅ 1080x1920 recommended

### Instagram Reels
- ✅ 9:16 format preferred
- ✅ Up to 90 seconds
- ✅ 1080x1920 recommended

### Facebook Reels
- ✅ 9:16 format preferred
- ✅ Up to 60 seconds
- ✅ 1080x1920 recommended

## Advanced: Understanding the FFmpeg Filter

The vertical conversion uses this FFmpeg filter:

```bash
[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black[main];
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];
[bg][main]overlay=(W-w)/2:(H-h)/2
```

**What it does:**
1. **Main video**: Scales to fit 1080x1920, adds padding
2. **Background**: Scales to fill 1080x1920, applies blur
3. **Overlay**: Centers main video over blurred background

**Blur settings:**
- Radius: 1/20th of video dimension (adaptive)
- Power: 1 (moderate blur)
- Applied to both luma (brightness) and chroma (color)

## Examples

### Example 1: Music Video
```bash
python main.py "My Song.mp4" --vertical --max-clips 3 --max-duration 30
```
**Output**: 3 clips, 30 seconds max each, vertical format
**Use case**: YouTube Shorts promotion for music release

### Example 2: Podcast Highlights
```bash
python main.py podcast_episode.mp4 --vertical --max-clips 5 --whisper-model medium
```
**Output**: 5 best moments, better transcription, vertical format
**Use case**: Social media clips from podcast

### Example 3: Tutorial Snippets
```bash
python main.py tutorial.mp4 --vertical --min-duration 20 --max-duration 45
```
**Output**: Clips between 20-45 seconds, vertical format
**Use case**: Educational content for Reels/Shorts

## Cost Consideration

Vertical conversion does NOT increase API costs:
- Transcription: Same (uses same audio)
- Claude API: Same (uses same transcript)
- Only difference: Local FFmpeg processing time

So feel free to use `--vertical` - it won't cost you more! 💰

---

**Ready to create phone-optimized Shorts? Just add `--vertical` to your command!** 📱
