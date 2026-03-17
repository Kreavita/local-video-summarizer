#!/usr/bin/env python
import torch

if torch.cuda.is_available():
    print(f"CUDA available: Yes")
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")
else:
    print("CUDA available: No")
    print("Whisper will run on CPU (install torch with CUDA for GPU acceleration)")
    print("  pip install torch --index-url https://download.pytorch.org/whl/cu121")
