import argparse

from stemslib.models import default_model_for_backend
from stemslib.utils import DEFAULT_BACKEND, DEFAULT_EXCLUDE, DEFAULT_OUTPUT_DIR, STEM_NAMES, SUPPORTED_BACKENDS


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pedal-steel-stems",
        description="AI-powered stem separation for pedal steel guitar practice",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_cmd = subparsers.add_parser("split", help="Separate a single audio file into stems")
    split_cmd.add_argument("file", help="Path to the audio file")
    split_cmd.add_argument("--out", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    split_cmd.add_argument("--backend", choices=SUPPORTED_BACKENDS, default=DEFAULT_BACKEND,
                           help=f"Separation backend to use (default: {DEFAULT_BACKEND})")
    split_cmd.add_argument("--model", default=None,
                           help=("Model name to use. Defaults depend on backend: demucs defaults to "
                                 f"{default_model_for_backend('demucs')}; audio-separator defaults to "
                                 f"{default_model_for_backend('audio-separator')}."))
    split_cmd.add_argument("--device", default=None,
                           help="Optional torch device (for example: mps or cpu)")
    split_cmd.add_argument("--mix", action="store_true", help="Also create a mix excluding stems")
    split_cmd.add_argument("--exclude", nargs="+", default=DEFAULT_EXCLUDE, choices=STEM_NAMES,
                           help="Stems to exclude when creating the mix (default: guitar)")

    batch_cmd = subparsers.add_parser("batch", help="Separate all audio files in a folder")
    batch_cmd.add_argument("folder", help="Path to the folder containing audio files")
    batch_cmd.add_argument("--out", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    batch_cmd.add_argument("--backend", choices=SUPPORTED_BACKENDS, default=DEFAULT_BACKEND,
                           help=f"Separation backend to use (default: {DEFAULT_BACKEND})")
    batch_cmd.add_argument("--model", default=None,
                           help=("Model name to use. Defaults depend on backend: demucs defaults to "
                                 f"{default_model_for_backend('demucs')}; audio-separator defaults to "
                                 f"{default_model_for_backend('audio-separator')}."))
    batch_cmd.add_argument("--device", default=None,
                           help="Optional torch device (for example: mps or cpu)")
    batch_cmd.add_argument("--mix", action="store_true", help="Also create mixes excluding stems")
    batch_cmd.add_argument("--exclude", nargs="+", default=DEFAULT_EXCLUDE, choices=STEM_NAMES,
                           help="Stems to exclude when creating the mixes (default: guitar)")

    mix_cmd = subparsers.add_parser("mix", help="Recombine stems excluding specified instruments")
    mix_cmd.add_argument("stems_folder", help="Path to the folder containing separated stems")
    mix_cmd.add_argument("--output", help="Output file path (auto-generated if not specified)")
    mix_cmd.add_argument("--exclude", nargs="+", default=DEFAULT_EXCLUDE, choices=STEM_NAMES,
                         help="Stems to exclude when creating the mix (default: guitar)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "split":
        from stemslib.splitter import split_file
        stems_folder = split_file(args.file, args.out, backend=args.backend, model=args.model, device=args.device)
        print(f"Stems saved to: {stems_folder}")
        if args.mix:
            print(f"Creating mix excluding: {args.exclude}")
            from stemslib.mixer import mix_stems
            mix_stems(stems_folder, exclude=args.exclude)
            print(f"Mix audio saved to: {stems_folder}")
    elif args.command == "mix":
        from stemslib.mixer import mix_stems
        output_path = mix_stems(args.stems_folder, exclude=args.exclude, output_path=args.output)
        print(f"Mixed audio saved to: {output_path}")
    elif args.command == "batch":
        from stemslib.batch import batch_process
        batch_process(args.folder, args.out, backend=args.backend, model=args.model, device=args.device,
                     mix=args.mix, exclude=args.exclude)
    else:
        print(f"Command '{args.command}' not implemented yet.")


if __name__ == "__main__":
    main()