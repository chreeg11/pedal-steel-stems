# Supported audio file extensions
SUPPORTED_FORMATS = [".mp3", ".wav", ".flac", ".ogg", ".m4a"]

# Available stems from the htdemucs_6s model
STEM_NAMES = ["vocals", "drums", "bass", "guitar", "piano", "other"]

# Default Demucs model
DEFAULT_MODEL = "htdemucs_6s"
DEFAULT_BACKEND = "demucs"
SUPPORTED_BACKENDS = ["demucs", "audio-separator"]

MODEL_ALIASES = {
    "demucs": {
        "htdemucs_6s": "htdemucs_6s",
        "htdemucs_ft": "htdemucs_ft",
    },
    "audio-separator": {
        "mdx23": "UVR-MDX-NET-Inst_HQ_3.onnx",
        "mdx23-kara": "UVR_MDXNET_KARA_2.onnx",
        "reformer": "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        "roformer": "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        "melband-roformer": "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        "melband-roformer-kim-vocals": "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        "bs-roformer": "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        "bs_roformer": "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
    },
}


def resolve_model_name(backend_name, model_name):
    backend_name = (backend_name or DEFAULT_BACKEND).strip().lower()
    if model_name is None:
        if backend_name == "demucs":
            return DEFAULT_MODEL
        return "mdx23"

    normalized = str(model_name).strip()
    alias_map = MODEL_ALIASES.get(backend_name, {})
    return alias_map.get(normalized.lower(), normalized)


# Default output directory
DEFAULT_OUTPUT_DIR = "output"

# Default stems to exclude when mixing
DEFAULT_EXCLUDE = ["guitar"]