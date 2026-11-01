from .utils import resolve_model_name


def default_model_for_backend(backend_name):
    backend_name = (backend_name or "demucs").strip().lower()
    if backend_name == "demucs":
        return "htdemucs_6s"
    if backend_name == "audio-separator":
        return "mdx23"
    return resolve_model_name(backend_name, None)
