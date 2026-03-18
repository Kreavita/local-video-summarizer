import re
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
        RequestBlocked,
    )
    YOUTUBE_TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    YOUTUBE_TRANSCRIPT_API_AVAILABLE = False


def extract_video_id(url: str) -> str | None:
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_transcript(transcript_data: list, include_timestamps: bool = True) -> str:
    if include_timestamps:
        lines = []
        for entry in transcript_data:
            start = entry.get('start', 0)
            duration = entry.get('duration', 0)
            text = entry.get('text', '').strip()
            if text:
                lines.append(f"[{start:.1f}s - {start + duration:.1f}s] {text}")
        return '\n'.join(lines)
    else:
        return ' '.join(entry.get('text', '').strip() for entry in transcript_data if entry.get('text'))


def fetch_youtube_transcript(
    url: str,
    language: str | None = None,
    include_timestamps: bool = True,
    languages: list[str] | None = None,
) -> tuple[str | None, str | None]:
    if not YOUTUBE_TRANSCRIPT_API_AVAILABLE:
        return None, "youtube-transcript-api not installed"

    video_id = extract_video_id(url)
    if not video_id:
        return None, "Could not extract video ID from URL"

    if languages is None:
        languages = ['en'] if language is None else [language]

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=languages)
        
        transcript_data = fetched_transcript.to_raw_data()
        formatted = format_transcript(transcript_data, include_timestamps)
        
        source = "manual" if not fetched_transcript.is_generated else "generated"
        lang = fetched_transcript.language_code
        return formatted, f"Success ({source}, {lang})"

    except NoTranscriptFound:
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)
            
            for t in transcript_list:
                if not t.is_generated:
                    fetched = t.fetch()
                    transcript_data = fetched.to_raw_data()
                    formatted = format_transcript(transcript_data, include_timestamps)
                    return formatted, f"Success (manual, {t.language_code})"
            
            for t in transcript_list:
                fetched = t.fetch()
                transcript_data = fetched.to_raw_data()
                formatted = format_transcript(transcript_data, include_timestamps)
                return formatted, f"Success (generated, {t.language_code})"
        except Exception:
            pass
        
        return None, "No transcript found for this video"
    
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video"
    except VideoUnavailable:
        return None, "Video is unavailable"
    except RequestBlocked:
        return None, "Request blocked - YouTube blocked this IP"
    except Exception as e:
        return None, f"Error: {str(e)}"


def has_transcript_available(url: str) -> bool:
    if not YOUTUBE_TRANSCRIPT_API_AVAILABLE:
        return False

    video_id = extract_video_id(url)
    if not video_id:
        return False

    try:
        ytt_api = YouTubeTranscriptApi()
        ytt_api.list(video_id)
        return True
    except Exception:
        return False
