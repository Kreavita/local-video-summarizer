import requests
from .config import OPENAI_BASE_URL, CONTEXT_WINDOW

_default_model = None


def fetch_default_model():
    global _default_model
    if _default_model is not None:
        return _default_model
    from .config import OPENAI_MODEL
    if OPENAI_MODEL:
        _default_model = OPENAI_MODEL
        return _default_model
    response = requests.get(f"{OPENAI_BASE_URL}/models", timeout=10)
    response.raise_for_status()
    data = response.json()
    models = data.get("data", [])
    if not models:
        raise RuntimeError("No models available at OpenAI-compatible endpoint")
    _default_model = models[0]["id"]
    return _default_model


def format_metadata(metadata: dict) -> str:
    """Format video metadata for the prompt."""
    upload_date = metadata.get('upload_date', '')
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

    lines = [
        "Video Information:",
        f"- Title: {metadata.get('title', 'N/A')}",
        f"- Channel: {metadata.get('channel', 'N/A')}",
        f"- Upload Date: {upload_date or 'N/A'}",
    ]
    desc = metadata.get('description', '').strip()
    if desc:
        lines.append(f"- Description: {desc[:500]}{'...' if len(desc) > 500 else ''}")
    return '\n'.join(lines)


def summarize_text(text: str, prompt: str, model: str = None, metadata: dict = None, context_window: int = None) -> str:
    """Send transcript to LLM and get summary."""
    if not model:
        model = fetch_default_model()
    max_tokens = context_window or CONTEXT_WINDOW

    metadata_section = format_metadata(metadata) if metadata else ""

    if metadata_section:
        user_content = f"{metadata_section}\n\nTranscript:\n{text}"
    else:
        user_content = f"Transcript:\n{text}"

    response = requests.post(
        f"{OPENAI_BASE_URL}/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_content}
            ],
            "max_tokens": max_tokens,
            "stream": False
        }
    )

    if not response.ok:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}: {response.text}")
        except ValueError:
            error_msg = f"HTTP {response.status_code}: {response.text}"
        raise RuntimeError(f"API error: {error_msg}")

    result = response.json()

    choices = result.get("choices", [])
    if not choices:
        raise RuntimeError("API response contains no choices")

    summary = choices[0].get("message", {}).get("content", "")

    return summary
