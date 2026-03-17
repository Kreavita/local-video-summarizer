import whisper
import torch


def check_cuda() -> str:
    """Check CUDA availability and return device info."""
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        cuda_ver = torch.version.cuda
        return f"cuda ({device_name}, CUDA {cuda_ver})"
    return "cpu"


def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """Transcribe audio file using Whisper."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {check_cuda()}")
    model = whisper.load_model(model_size, device=device)
    result = model.transcribe(audio_path, verbose=False)
    return result["text"]
