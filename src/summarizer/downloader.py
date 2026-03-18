import yt_dlp
import os
import subprocess
import re
from pathlib import Path
from typing import Generator


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


def download_audio_progress(url: str, output_path: str = ".") -> tuple[str, dict, Generator[dict, None, None]]:
    """Download audio from YouTube with progress updates."""
    video_id = None
    
    class ProgressHook:
        def __init__(self):
            self.progress: list[dict] = []
        
        def __call__(self, info):
            if info['status'] == 'downloading':
                total = info.get('total_bytes') or info.get('total_bytes_estimate', 0)
                downloaded = info.get('downloaded_bytes', 0)
                speed = info.get('speed', 0)
                eta = info.get('eta', 0)
                
                if total > 0:
                    pct = downloaded / total
                    speed_str = f"{speed / 1024 / 1024:.2f}MB/s" if speed else "N/A"
                    eta_str = f"{eta // 60}m {eta % 60}s" if eta else "N/A"
                    yield {
                        "progress": pct,
                        "text": f"Downloading... {pct * 100:.1f}% ({speed_str}, ETA: {eta_str})"
                    }
            elif info['status'] == 'finished':
                yield {"progress": 1.0, "text": "Download complete"}
                video_id = info.get('filename', '').split('/')[-1].split('.')[0]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        'progress_hooks': [ProgressHook()],
    }

    progress_hook = ProgressHook()
    ydl_opts['progress_hooks'] = [progress_hook]

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
    
    def progress_gen():
        yield from progress_hook.progress
        yield {"progress": 1.0, "text": "Download complete"}
    
    return audio_file, metadata, progress_gen()


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
