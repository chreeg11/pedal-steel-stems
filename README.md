# pedal-steel-stems

Small Python CLI for splitting an audio file into Demucs stems and optionally remixing those stems with selected instruments removed.

## macOS setup

This project works on macOS with Homebrew Python and `ffmpeg`.

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
python cli.py split /path/to/song.wav --out output --model htdemucs_ft
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
python cli.py batch /path/to/folder --out output --model htdemucs_ft
```

Create a new mix from an existing stems folder:

```bash
python cli.py mix output/htdemucs_6s/song_name --exclude guitar --output output/song_name_no_guitar.wav
```

## Notes

- Supported input formats: `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`
- Model defaults to `htdemucs_6s`; pass `--model` to override.
- The first `split` run downloads the Demucs model weights.
- Output stems are written to `output/<model>/<input-file-name>/`
