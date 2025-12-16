"""
Transcription module using OpenAI Whisper for speech-to-text conversion.
"""

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

    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print("Transcribing audio...")
    result = model.transcribe(audio_path, verbose=False)

    return result


def save_transcript(transcript: dict, output_path: str):
    """
    Save transcript to JSON file.

    Args:
        transcript: Whisper transcript dictionary
        output_path: Path where to save the JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)
