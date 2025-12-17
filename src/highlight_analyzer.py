"""
Highlight analysis module using Claude API to identify best clip moments.
"""

import anthropic
import json
import re
from config import get_api_key


def build_analysis_prompt(transcript: dict, max_clips: int, min_duration: int, max_duration: int) -> str:
    """
    Build the prompt for Claude API.

    Args:
        transcript: Whisper transcript dictionary
        max_clips: Maximum number of clips to suggest
        min_duration: Minimum clip duration in seconds
        max_duration: Maximum clip duration in seconds

    Returns:
        Formatted prompt string for Claude
    """
    full_text = transcript.get('text', '')
    segments = transcript.get('segments', [])

    # Format segments with timestamps
    formatted_segments = []
    for seg in segments:
        formatted_segments.append(
            f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}"
        )

    segments_text = "\n".join(formatted_segments)

    prompt = f"""You are an expert YouTube Shorts creator and copywriter. Analyze this video transcript and identify the {max_clips} BEST moments to turn into viral YouTube Shorts (15-60 second clips).

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
3. title (catchy YouTube title, 5-8 words, capitalize key words)
4. hook (attention-grabbing opening line, 5-10 words, creates curiosity)
5. description (full YouTube Shorts description, 2-3 sentences, include relevant hashtags)
6. thumbnail_text (bold text for thumbnail overlay, 2-4 words, ALL CAPS if impactful)
7. reason (why this moment works as a Short)

EXAMPLES OF GOOD OUTPUTS:
- hook: "Wait until you see what happens next..."
- description: "The most unexpected moment from today's session! This is why you should never assume anything. #Shorts #Viral #Unexpected"
- thumbnail_text: "NO WAY!"

Return your response as a JSON array ONLY (no other text):
[
  {{
    "start_time": 45.2,
    "end_time": 72.1,
    "title": "Epic Fail Moment Caught On Camera",
    "hook": "You won't believe this happened...",
    "description": "The most epic fail you'll see today! Watch what happens when confidence meets reality. This is pure comedy gold! #Shorts #EpicFail #Funny #Viral",
    "thumbnail_text": "EPIC FAIL",
    "reason": "High energy moment with visual payoff and standalone story"
  }}
]"""

    return prompt


def analyze_highlights(
    transcript: dict,
    max_clips: int = 5,
    min_duration: int = 15,
    max_duration: int = 60
) -> list:
    """
    Use Claude API to analyze transcript and find highlights.

    Args:
        transcript: Whisper transcript dict
        max_clips: Maximum number of clips to suggest
        min_duration: Minimum clip length in seconds
        max_duration: Maximum clip length in seconds

    Returns:
        List of clip dicts with start_time, end_time, title, hook, description,
        thumbnail_text, reason

    Raises:
        Exception: If Claude API call fails
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
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if json_match:
        clips = json.loads(json_match.group(0))
    else:
        clips = json.loads(response_text)

    return clips
