# pedal-steel-stems

Small Python CLI for splitting an audio file into stems from multiple open-source backends and optionally remixing those stems with selected instruments removed.

## macOS setup

This project works on macOS with Homebrew Python and `ffmpeg`.

Use Python 3.11 for the most stable Demucs + audio-separator/RoFormer setup on Apple Silicon. Python 3.14 has caused `beartype`/RoFormer compatibility failures with some checkpoints.

```bash
brew install python@3.11 ffmpeg
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `python3.11` is not on your `PATH`, use the Homebrew path directly:

```bash
/opt/homebrew/bin/python3.11 -m venv .venv
```

## Usage

Show commands:

```bash
source .venv/bin/activate
python cli.py --help
```

Split one file into stems:

```bash
python cli.py split /path/to/song.wav --out output
```

Split one file with a specific Demucs model:

```bash
python cli.py split /path/to/song.wav --out output --backend demucs --model htdemucs_ft
```

Split one file with the audio-separator backend and an MDX model. On macOS, install the CPU extra so the ONNX runtime is present:

```bash
python -m pip install "audio-separator[cpu]"
python cli.py split /path/to/song.wav --out output --backend audio-separator --model mdx23 --device mps
```

Split one file with a RoFormer checkpoint through audio-separator:

```bash
python cli.py split /path/to/song.wav --out output --backend audio-separator --model roformer --device mps
```

Split and also create a mix without pedal steel/guitar:

```bash
python cli.py split /path/to/song.wav --out output --mix --exclude guitar
```

Batch process a folder:

```bash
python cli.py batch /path/to/folder --out output --mix --exclude guitar
```

Batch process with a specific model:

```bash
python cli.py batch /path/to/folder --out output --backend demucs --model htdemucs_ft
```

Batch process with the audio-separator backend on Apple Silicon:

```bash
python cli.py batch /path/to/folder --out output --backend audio-separator --model mdx23 --device mps
```

Create a new mix from an existing stems folder:

```bash
python cli.py mix output/htdemucs_6s/song_name --exclude guitar --output output/song_name_no_guitar.wav
```

## Notes

- Supported input formats: `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`
- Supported backends: `demucs` and `audio-separator`.
- Model defaults depend on backend (`demucs` defaults to `htdemucs_6s`; `audio-separator` defaults to `mdx23`).
- The first `split` run downloads the selected model weights.
- Output stems are written under `output/<backend>/<model>/<input-file-name>/` for Demucs, or a normalized stem folder for audio-separator outputs.
