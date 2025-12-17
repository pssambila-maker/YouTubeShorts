# Full Video Metadata Examples

The app now generates **complete YouTube metadata** for your entire video, perfect for when you upload the full music video or long-form content!

## What Gets Generated

For every video, you get two types of content:

### 1. Full Video Metadata (NEW!)
Professional YouTube metadata for the complete video upload

### 2. Shorts Clips Metadata (Existing)
Individual metadata for each 15-60 second highlight clip

---

## Example Output: Music Video

### Full Video Metadata

**File**: `output/reports/my_song_metadata.txt`

```
======================================================================
FULL VIDEO YOUTUBE METADATA
======================================================================

TITLE:
Lost in the City - Official Music Video | Emotional Pop Ballad 2025

DESCRIPTION:
Experience the journey of finding yourself in the chaos of city life with "Lost in the City."
This emotional pop ballad combines powerful vocals with cinematic visuals to tell a story of
self-discovery and resilience. Perfect for fans of emotional pop, indie music, and contemporary
ballads.

Shot on location in downtown LA, this official music video captures the raw emotion and
vulnerability of feeling lost while searching for your place in the world. The song explores
themes of loneliness, hope, and the courage it takes to keep moving forward.

Stream "Lost in the City" on all platforms: [Your Links Here]
Follow us: [Your Social Links]

#MusicVideo #PopMusic #EmotionalSong #NewMusic2025 #IndieMusic #PopBallad #OfficialMusicVideo
#EmotionalMusic #NewRelease #MusicDiscovery #IndieArtist #PopSong #MusicLovers

TAGS:
music video, pop music, emotional song, 2025 music, new music, indie pop, pop ballad,
official music video, emotional music, indie music, contemporary pop, new release,
music discovery, independent artist, pop songs 2025, emotional ballad, music lovers,
trending music, viral music, new artist

THUMBNAIL TEXT:
LOST IN THE CITY

CATEGORY:
Music

KEY MOMENTS / CHAPTERS:
  0:00 - Intro/Opening Scene
  0:30 - First Verse Begins
  1:15 - Pre-Chorus Build
  1:45 - Chorus Drop
  2:30 - Second Verse
  3:15 - Bridge/Emotional Peak
  3:45 - Final Chorus
  4:15 - Outro/Ending Scene

======================================================================
```

---

## Example: Podcast/Interview

### Full Video Metadata

```
TITLE:
How I Built a $10M Business in 3 Years | Entrepreneur Success Story

DESCRIPTION:
In this exclusive interview, successful entrepreneur Sarah Chen shares her incredible journey
from startup founder to building a multi-million dollar business. Learn the exact strategies,
mindset shifts, and tactical advice that helped her scale her company to $10M in just three years.

In this conversation, we cover:
- The pivotal moment that changed everything
- How to overcome self-doubt and imposter syndrome
- Practical steps for scaling from 6 to 7 figures
- Common mistakes that cost entrepreneurs millions
- Daily habits of highly successful business owners

Whether you're just starting out or looking to take your business to the next level, this
episode is packed with actionable insights you can implement today.

#Entrepreneurship #BusinessSuccess #StartupStory #MillionaireMinds #BusinessGrowth
#SuccessStory #Entrepreneur #BusinessTips #Motivation

TAGS:
entrepreneurship, business success, startup story, how to build a business, entrepreneur
interview, business growth, startup tips, millionaire mindset, success story, business advice,
small business, scaling business, business motivation, startup founder, entrepreneur tips

THUMBNAIL TEXT:
$10M IN 3 YEARS

CATEGORY:
Education

KEY MOMENTS / CHAPTERS:
  0:00 - Introduction
  2:15 - Sarah's Background Story
  5:30 - The Turning Point
  12:45 - Scaling Strategy Revealed
  18:20 - Biggest Mistakes
  25:10 - Daily Success Habits
  30:45 - Final Advice for Entrepreneurs
```

---

## How to Use This Metadata

### For Full Video Upload:

1. **Open** `output/reports/your_video_metadata.txt`
2. **Copy** the title → Paste into YouTube title field
3. **Copy** the description → Paste into YouTube description
4. **Copy** the tags → Paste into YouTube tags (comma-separated)
5. **Use** the thumbnail text → Create custom thumbnail
6. **Select** the suggested category in YouTube upload
7. **Add** key moments as YouTube chapters (copy timestamp format exactly)

### Visual Guide:

```
YouTube Upload Page:

Title: [Paste from "TITLE:" section]
┌─────────────────────────────────────────────┐
│ Lost in the City - Official Music Video... │
└─────────────────────────────────────────────┘

Description: [Paste from "DESCRIPTION:" section]
┌─────────────────────────────────────────────┐
│ Experience the journey of finding          │
│ yourself in the chaos of city life...      │
│                                             │
│ [Full description with hashtags]           │
└─────────────────────────────────────────────┘

Tags: [Paste from "TAGS:" section]
┌─────────────────────────────────────────────┐
│ music video, pop music, emotional song,... │
└─────────────────────────────────────────────┘

Category: [Select from "CATEGORY:" suggestion]
☑ Music

Thumbnail: [Use "THUMBNAIL TEXT:" for overlay]
```

---

## Comparison: Full Video vs Shorts

| Feature | Full Video Metadata | Shorts Clip Metadata |
|---------|-------------------|---------------------|
| Title | 50-70 chars, SEO-optimized | 5-8 words, catchy |
| Description | 3-5 paragraphs, keywords | 2-3 sentences, hooks |
| Purpose | Long-form upload | Viral clips |
| Hashtags | 10-15 strategic tags | 4-6 trending tags |
| Chapters | Yes (key moments) | N/A |
| Category | YouTube category | N/A |
| SEO Focus | High (discoverability) | Medium (engagement) |

---

## Files Generated

After running the app, you'll find:

```
output/reports/
├── your_video_metadata.json          # Full video (machine-readable)
├── your_video_metadata.txt           # Full video (human-readable) ✨ NEW
├── your_video_clips.json             # Shorts clips (machine-readable)
└── your_video_clips.txt              # Shorts clips (human-readable)
```

---

## Tips for Best Results

### For Music Videos:

**Full Video Upload:**
- Use the generated title for the main upload
- Description includes streaming links section (add your links)
- Tags help with music discovery
- Chapters mark chorus, verses, bridge

**Shorts Clips:**
- Use for TikTok, Instagram Reels, YouTube Shorts
- Each clip promotes the full video
- Include link to full video in descriptions

### For Podcasts/Interviews:

**Full Video Upload:**
- Title optimized for search (includes guest name, topic)
- Description includes topics covered
- Chapters help viewers jump to specific topics
- Tags help podcast discoverability

**Shorts Clips:**
- Best moments extracted automatically
- Each clip is shareable standalone content
- Drives traffic back to full episode

---

## Cost Estimate

Generating full video metadata adds minimal cost:

**Previous (Shorts only):**
- Transcription: ~3,000 tokens
- Highlights: ~500 tokens
- **Total: ~$0.02**

**Now (Full video + Shorts):**
- Transcription: ~3,000 tokens (same)
- **Full metadata: ~500 tokens** ← New
- Highlights: ~500 tokens (same)
- **Total: ~$0.03**

**Additional cost: ~$0.01 per video**

Worth it for professional YouTube metadata! 💰

---

## Advanced: JSON Format

The `video_name_metadata.json` file contains:

```json
{
  "title": "Lost in the City - Official Music Video | Emotional Pop Ballad 2025",
  "description": "Experience the journey of finding yourself...",
  "tags": [
    "music video",
    "pop music",
    "emotional song",
    "2025 music",
    ...
  ],
  "thumbnail_text": "LOST IN THE CITY",
  "category": "Music",
  "key_moments": [
    {"timestamp": "0:00", "description": "Intro/Opening Scene"},
    {"timestamp": "0:30", "description": "First Verse Begins"},
    ...
  ]
}
```

Use this JSON for:
- Automation scripts
- Batch video uploads
- YouTube API integration
- Analytics tracking

---

## Example Workflow

### Complete YouTube Upload Workflow:

1. **Run the app:**
   ```bash
   python main.py my_music_video.mp4 --vertical --max-clips 3
   ```

2. **Upload full video:**
   - Use metadata from `my_music_video_metadata.txt`
   - Create thumbnail with suggested text
   - Add chapters from key moments

3. **Upload Shorts:**
   - Use clips from `output/clips/`
   - Each has its own title, description, hook from `my_music_video_clips.txt`
   - Link back to full video

4. **Cross-promote:**
   - Pin comment on full video linking to Shorts
   - Add full video link in Shorts descriptions
   - Maximum discoverability! 🚀

---

**Your complete YouTube content strategy, automated!** 🎬📊
