from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from demucs.separate import main as separate

from .utils import DEFAULT_MODEL, STEM_NAMES, resolve_model_name


class BaseBackend:
    name = "base"

    def supported_models(self):
        return []

    def separate_file(self, input_path, output_dir, model=None, device=None, **kwargs):
        raise NotImplementedError


class DemucsBackend(BaseBackend):
    name = "demucs"

    def supported_models(self):
        return ["htdemucs_6s", "htdemucs_ft"]

    def separate_file(self, input_path, output_dir, model=None, device=None, **kwargs):
        resolved_model = resolve_model_name(self.name, model or DEFAULT_MODEL)
        input_path = Path(input_path).resolve()
        output_dir = Path(output_dir).resolve()

        if not input_path.exists() or not input_path.is_file():
            raise FileNotFoundError(f"File not found: {input_path}")

        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Separating: {input_path.name} [{self.name}/{resolved_model}]")

        args = ["--name", resolved_model, "--out", str(output_dir)]
        if device:
            args.extend(["--device", str(device)])
        args.append(str(input_path))
        separate(args)

        return output_dir / resolved_model / input_path.stem


class AudioSeparatorBackend(BaseBackend):
    name = "audio-separator"

    def supported_models(self):
        return [
            "mdx23",
            "mdx23-kara",
            "reformer",
            "roformer",
            "melband-roformer",
            "melband-roformer-kim-vocals",
            "bs-roformer",
            "UVR-MDX-NET-Inst_HQ_3.onnx",
            "UVR_MDXNET_KARA_2.onnx",
            "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        ]

    def separate_file(self, input_path, output_dir, model=None, device=None, **kwargs):
        resolved_model = resolve_model_name(self.name, model or "mdx23")
        roformer_models = {
            "reformer",
            "roformer",
            "melband-roformer",
            "melband-roformer-kim-vocals",
            "bs-roformer",
            "bs_roformer",
            "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        }
        if sys.version_info >= (3, 14) and resolved_model.lower() in {m.lower() for m in roformer_models}:
            raise RuntimeError(
                "The audio-separator RoFormer stack is not compatible with Python 3.14 on Apple Silicon. "
                "Create a Python 3.11 virtual environment and reinstall dependencies before running "
                f"the audio-separator backend with model '{model or 'reformer'}'."
            )

        try:
            from audio_separator.separator import Separator
        except ImportError as exc:  # pragma: no cover - exercised only when optional backend not installed
            raise RuntimeError(
                "audio-separator runtime dependencies are missing. Install them with "
                "`python -m pip install 'audio-separator[cpu]'` or the project requirements file "
                "to use the audio-separator backend."
            ) from exc

        resolved_model = resolve_model_name(self.name, model or "mdx23")
        input_path = Path(input_path).resolve()
        output_dir = Path(output_dir).resolve()

        if not input_path.exists() or not input_path.is_file():
            raise FileNotFoundError(f"File not found: {input_path}")

        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Separating: {input_path.name} [{self.name}/{resolved_model}]")

        separator = Separator(output_dir=str(output_dir))
        if device:
            try:
                separator.device = device
            except AttributeError:
                pass

        separator.load_model(model_filename=resolved_model)
        output_files = separator.separate(str(input_path))
        return _normalize_audio_separator_output(output_files, input_path, output_dir)


def _normalize_audio_separator_output(output_files, input_path, output_dir):
    if isinstance(output_files, (str, Path)):
        output_files = [output_files]

    stems_dir = output_dir / "audio-separator" / input_path.stem
    stems_dir.mkdir(parents=True, exist_ok=True)

    exported = []
    for output_file in output_files or []:
        path = Path(output_file)
        if path.exists():
            exported.append(path)

    if not exported:
        exported = [
            path
            for path in output_dir.rglob("*")
            if path.is_file() and path.name.startswith(f"{input_path.stem}")
        ]

    if not exported:
        raise RuntimeError(f"audio-separator did not produce any output files for: {input_path}")

    for output_file in exported:
        stem_name = _guess_stem_name(output_file.name)
        if stem_name is None:
            continue
        target = stems_dir / f"{stem_name}.wav"
        shutil.copy2(output_file, target)

    if not any(stems_dir.iterdir()):
        raise RuntimeError(
            f"audio-separator output could not be normalized into stem files for: {input_path}"
        )

    return stems_dir


def _guess_stem_name(filename: str):
    normalized = Path(filename).stem.lower()
    tokens = set(re.sub(r"[^a-z0-9]+", " ", normalized).split())

    for stem_name in STEM_NAMES:
        if stem_name in tokens:
            return stem_name

    if "vocals" in tokens:
        return "vocals"
    if "instrumental" in tokens or "accompaniment" in tokens:
        return "other"
    return None


BACKENDS = {
    DemucsBackend.name: DemucsBackend(),
    AudioSeparatorBackend.name: AudioSeparatorBackend(),
}


def get_backend(name):
    backend_name = (name or "demucs").strip().lower()
    if backend_name not in BACKENDS:
        valid = ", ".join(sorted(BACKENDS.keys()))
        raise ValueError(f"Unsupported backend '{name}'. Valid values: {valid}")
    return BACKENDS[backend_name]
