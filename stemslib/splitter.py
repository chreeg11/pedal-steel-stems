from .backends import get_backend
from .utils import DEFAULT_BACKEND, resolve_model_name


def split_file(input_path, output_dir, model=None, backend=DEFAULT_BACKEND, device=None):
    """
    Separate a single audio file into stems using the selected backend.

    Args:
        input_path (str): Path to the input audio file.
        output_dir (str): Directory where the separated stems will be saved.
        model (str): Backend-specific model name.
        backend (str): Separation backend name (for example: demucs or audio-separator).
        device (str): Optional torch device, such as mps or cpu.
    """
    backend_impl = get_backend(backend)
    resolved_model = resolve_model_name(backend, model) if model is not None else None
    return backend_impl.separate_file(
        input_path=input_path,
        output_dir=output_dir,
        model=resolved_model,
        device=device,
    )