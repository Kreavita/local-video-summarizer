import yt_dlp
import os


def get_video_metadata(url: str) -> dict:
    """Get video metadata."""
    ydl_opts = {'format': 'bestaudio/best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
    metadata = {
        'id': info.get('id', 'unknown'),
        'title': info.get('title', ''),
        'channel': info.get('channel', ''),
        'upload_date': info.get('upload_date', ''),
        'description': info.get('description', ''),
        'duration': info.get('duration', 0),
        'view_count': info.get('view_count', 0),
        'like_count': info.get('like_count', 0),
        'categories': info.get('categories', []),
        'tags': info.get('tags', []),
    }
    
    return metadata


def download_audio(url: str, output_path: str = ".") -> tuple[str, dict]:
    """Download audio from YouTube video and return audio path + metadata."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info['id']
        ext = info.get('ext', 'm4a')
        audio_file = os.path.join(output_path, f"{video_id}.{ext}")
        
        metadata = {
            'id': info.get('id', 'unknown'),
            'title': info.get('title', ''),
            'channel': info.get('channel', ''),
            'upload_date': info.get('upload_date', ''),
            'description': info.get('description', ''),
            'duration': info.get('duration', 0),
            'view_count': info.get('view_count', 0),
            'like_count': info.get('like_count', 0),
            'categories': info.get('categories', []),
            'tags': info.get('tags', []),
        }
    
    return audio_file, metadata
