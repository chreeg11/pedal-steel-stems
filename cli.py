import argparse
from stemslib.utils import DEFAULT_OUTPUT_DIR, DEFAULT_EXCLUDE, STEM_NAMES

def build_parser():
    parser = argparse.ArgumentParser(prog="pedal-steel-stems",
                                     description="AI-powered stem separation for pedal steel guitar practice"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # split command
    split_cmd = subparsers.add_parser("split", help="Separate a single audil file into stems")
    split_cmd.add_argument("file", help="Path to the audio file")
    split_cmd.add_argument("--out", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    split_cmd.add_argument("--mix", action="store_true", help="Also create a mix excluding stems")
    split_cmd.add_argument("--exclude", nargs="+", default=DEFAULT_EXCLUDE, choices=STEM_NAMES,
                           help="Stems to exclude when creating the mix (default: guitar)")
    
    # batch command
    batch_cmd = subparsers.add_parser("batch", help="Separate all audio files in a folder")
    batch_cmd.add_argument("folder", help="Path to the folder containing audio files")
    batch_cmd.add_argument("--out", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    batch_cmd.add_argument("--mix", action="store_true", help="Also create mixes excluding stems")
    batch_cmd.add_argument("--exclude", nargs="+", default=DEFAULT_EXCLUDE, choices=STEM_NAMES,
                           help="Stems to exclude when creating the mixes (default: guitar)")
    
    # mix command
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
        stems_folder = split_file(args.file, args.out)
        print (f"Stems saved to: {stems_folder}")
        if args.mix:
               print (f"Creating mix excluding: {args.exclude}")
               from stemslib.mixer import mix_stems
               mix_stems(stems_folder, exclude=args.exclude)
               print (f"Mix audio saved to: {stems_folder}")
    elif args.command == "mix":
        from stemslib.mixer import mix_stems
        output_path = mix_stems(args.stems_folder, exclude=args.exclude, output_path=args.output)
        print (f"Mixed audio saved to: {output_path}")
    elif args.command == "batch":
        from stemslib.batch import batch_process
        batch_process(args.folder, args.out, mix=args.mix, exclude=args.exclude)
    else:
        print (f"Command '{args.command}' not implemented yet.")

if __name__ == "__main__":
    main()