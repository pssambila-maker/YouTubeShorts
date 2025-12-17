"""
Video metadata generation module for creating full video YouTube content.
"""

import anthropic
import json
import re
from config import get_api_key


def generate_video_metadata(transcript: dict, video_name: str) -> dict:
    """
    Generate professional YouTube metadata for the full video.

    Args:
        transcript: Whisper transcript dictionary
        video_name: Name of the video file (without extension)

    Returns:
        Dict with title, description, tags, thumbnail_text, category suggestions
    """
    client = anthropic.Anthropic(api_key=get_api_key())

    full_text = transcript.get('text', '')
    segments = transcript.get('segments', [])

    # Get video duration
    if segments:
        duration_seconds = segments[-1]['end']
        duration_mins = int(duration_seconds // 60)
        duration_secs = int(duration_seconds % 60)
        duration_str = f"{duration_mins}:{duration_secs:02d}"
    else:
        duration_str = "unknown"

    prompt = f"""You are an expert YouTube SEO specialist and content strategist. Analyze this complete video transcript and create professional YouTube metadata that will maximize views and engagement.

VIDEO INFORMATION:
- File name: {video_name}
- Duration: {duration_str}

FULL TRANSCRIPT:
{full_text}

Based on this content, generate comprehensive YouTube metadata:

1. **title**: Professional YouTube title (50-70 characters, engaging, SEO-optimized, capitalize appropriately)
   - Include key themes or emotions
   - Make it clickable but not clickbait
   - Consider adding year or key descriptor if relevant

2. **description**: Full YouTube video description (3-5 paragraphs)
   - First 2-3 sentences are critical (appears in search)
   - Summarize what viewers will get from watching
   - Include relevant keywords naturally
   - Add 10-15 relevant hashtags at the end
   - Professional and engaging tone

3. **tags**: 15-20 relevant YouTube tags (comma-separated)
   - Mix of broad and specific tags
   - Include genre, mood, style, themes
   - Consider search intent

4. **thumbnail_text**: Bold text for video thumbnail (2-5 words)
   - ALL CAPS if impactful
   - Captures the essence of the video
   - Creates curiosity

5. **category**: Best YouTube category for this content
   - Options: Music, Entertainment, Education, People & Blogs, Film & Animation, Gaming, News & Politics, Howto & Style, Science & Technology, Nonprofits & Activism, Sports, Comedy

6. **key_moments**: 3-5 key moments/chapters with timestamps (format: MM:SS - description)

EXAMPLES OF GOOD OUTPUT:
- title: "Lost in the City - Official Music Video | Emotional Pop Ballad 2025"
- description: "Experience the journey of finding yourself in 'Lost in the City'... [detailed description] #MusicVideo #Pop #EmotionalSong"
- tags: "music video, pop music, emotional song, 2025 music, new music, indie pop"
- thumbnail_text: "LOST IN THE CITY"
- category: "Music"

Return your response as JSON ONLY (no other text):
{{
  "title": "Professional Title Here",
  "description": "Full description with multiple paragraphs and hashtags...",
  "tags": ["tag1", "tag2", "tag3", ...],
  "thumbnail_text": "THUMBNAIL TEXT",
  "category": "Music",
  "key_moments": [
    {{"timestamp": "0:00", "description": "Intro/Hook"}},
    {{"timestamp": "1:15", "description": "First Verse"}},
    {{"timestamp": "2:30", "description": "Chorus Drop"}}
  ]
}}"""

    print("Generating full video metadata with Claude AI...")
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
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        metadata = json.loads(json_match.group(0))
    else:
        metadata = json.loads(response_text)

    return metadata
