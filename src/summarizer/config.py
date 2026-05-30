import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:8080/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")
SUMMARY_PROMPT = os.getenv("SUMMARY_PROMPT", "Provide a concise summary of the following transcript in bullet points:")
CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", "32768"))
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "large-v3-turbo")
