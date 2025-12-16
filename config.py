"""
Configuration settings for YouTube Shorts Highlight Extractor.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
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
    """
    Load Anthropic API key from environment.

    Returns:
        str: The API key

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not found in environment
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in .env file. "
            "Please create a .env file with your API key."
        )
    return api_key


def create_output_dirs():
    """Create all output directories if they don't exist."""
    for dir_path in OUTPUT_DIRS.values():
        os.makedirs(dir_path, exist_ok=True)
