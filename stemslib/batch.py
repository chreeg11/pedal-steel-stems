from pathlib import Path

from .mixer import mix_stems
from .splitter import split_file
from .utils import DEFAULT_BACKEND, SUPPORTED_FORMATS


def batch_process(folder, output_dir, model=None, backend=DEFAULT_BACKEND, device=None, mix=False, exclude=None):
    """
    Process all audio files in a folder, separating them into stems and optionally creating mixes.

    Args:
        folder (str): Path to the folder containing audio files.
        output_dir (str): Directory to save the separated stems and mixes.
        model (str): Backend-specific model name to use.
        backend (str): Backend name (for example: demucs or audio-separator).
        device (str): Optional torch device, such as mps or cpu.
        mix (bool): Whether to create mixes excluding specified stems.
        exclude (list): List of stem names to exclude when creating mixes.
    """
    folder = Path(folder).resolve()
    output_dir = Path(output_dir).resolve()

    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Input folder not found: {folder}")

    audio_files = []
    for ext in SUPPORTED_FORMATS:
        audio_files.extend(folder.glob(f"*{ext}"))

    if not audio_files:
        print(f"No supported audio files found in: {folder}")
        return

    print(f"Found {len(audio_files)} audio file(s) to process")

    for audio_file in audio_files:
        print(f"\nProcessing: {audio_file.name}")
        stems_folder = split_file(str(audio_file), output_dir, model=model, backend=backend, device=device)
        print(f"  Stems saved to: {stems_folder}")

        if mix:
            mix_stems(stems_folder, exclude=exclude)