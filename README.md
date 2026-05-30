# Local Video Summarizer

Tool that extracts audio from local files or downloads audio from YouTube videos using [yt-dlp](https://github.com/yt-dlp/yt-dlp), transcribes using [faster-whisper](https://github.com/SYSTRAN/faster-whisper), and generates summaries via an OpenAI-compatible API.

## Features

- Download audio from YouTube videos ([yt-dlp](https://github.com/yt-dlp/yt-dlp))
- Or use local video/audio files (mp4, mkv, mov, mp3, m4a, etc.) (requires [FFmpeg](https://ffmpeg.org/) in PATH)
- Local transcription with [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- Customizable summary prompts via OpenAI-compatible API
- Beautiful Streamlit GUI or simple CLI interface

## Requirements

- [Python](https://www.python.org/) 3.10+
- [FFmpeg](https://ffmpeg.org/) (for audio processing)
- An OpenAI-compatible API endpoint running (default: `http://localhost:8080/v1`)
- *Optional for faster, GPU-accelerated Whisper: NVIDIA GPU with CUDA*

## OpenAI-compatible API Setup

The summarizer connects to any OpenAI-compatible API at the configured base URL.

### Default endpoint

The default endpoint is `http://localhost:8080/v1`. This could be:
- A local inference server (e.g., vLLM, LocalAI, llama.cpp, Ollama with OpenAI compatibility)
- A proxy like LiteLLM
- Any other OpenAI-compatible service

### Model auto-detection

The model is auto-detected from the `/v1/models` endpoint on startup. The first available model is used by default. To override, set `OPENAI_MODEL` in your `.env` file.

### Start your API server

If using Ollama with OpenAI compatibility:
```bash
ollama serve
# Accessible at http://localhost:11434/v1
```

## Installation

1. Clone the repository

2. Run the setup script to create virtual environment and install dependencies:

3. Activate the virtual environment:

**Linux/macOS:**
```bash
./setup.sh

# Activate the virtual environment
source venv/bin/activate
```

**Windows:**

> **Important**: Use Command Prompt (cmd), not PowerShell. If using PowerShell, you need to enable script execution:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

```cmd
.\setup.bat

REM Activate the virtual environment
venv\Scripts\activate
```

### GPU Support (Recommended)

For NVIDIA GPU acceleration, install torch with CUDA support :

```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Verify GPU is available:
```bash
python check_cuda.py
```

## Configuration

```bash
cp .env.example .env
# Then update your .env to your API endpoint and other settings
```

Copy or create a `.env` file with the following variables:

```env
# OpenAI-compatible API endpoint (default: http://localhost:8080/v1)
OPENAI_BASE_URL=http://localhost:8080/v1

# Model override (leave empty to auto-detect from /v1/models)
OPENAI_MODEL=

# Custom summary prompt (optional)
SUMMARY_PROMPT=Provide a concise summary of the following transcript in bullet points:

# Max tokens for response (default: 32768)
CONTEXT_WINDOW=32768

# Whisper model size (tiny, base, small, medium, large-v3-turbo, large-v3, turbo)
WHISPER_MODEL=large-v3-turbo
```

## Usage
### Web UI (Streamlit)

```bash
# Run summarizer without a url
summarizer
```

http://localhost:12820 will open in your browser.

### CLI

```bash
# Summarize a YouTube video
summarizer "https://www.youtube.com/watch?v=VIDEO_ID"

# Or use a local video/audio file
summarizer "/path/to/video.mov"
summarizer "/path/to/audio.m4a"
```

## CLI Options

| Option | Description |
|--------|-------------|
| `url` | YouTube video URL or local file path (optional - launches web UI if omitted) |
| `--prompt`, `-p` | Custom summary prompt |
| `--model`, `-m` | AI model name (auto-detected if not specified) |
| `--output`, `-o` | Output file for summary |
| `--whisper-model` | Whisper model size |
| `--keep-audio` | Keep downloaded audio file after processing |
| `--no-cache` | Disable transcript caching |


## Downloads and Caching

Audio files are downloaded to a temporary directory and automatically deleted after processing unless you use `--keep-audio`.

Transcripts are cached automatically to avoid re-transcribing the same video. Cache location: `~/.cache/yt_summarizer/`

To disable caching:
```bash
summarizer "URL" --no-cache
```

To keep the audio file:
```bash
summarizer "URL" --keep-audio
```
