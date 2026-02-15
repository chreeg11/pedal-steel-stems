from pathlib import Path
from demucs.separate import main as separate
from .utils import DEFAULT_MODEL

def split_file(input_path, output_dir):
    """
    Separate a single audio file into stems using Demucs.
    
    Args:
        input_path (str): Path to the input audio file.
        output_dir (str): Directory where the separated stems will be saved.
    """
    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Separating: {input_path.name}")
    
    separate([
        "--name", DEFAULT_MODEL,
        "--out", str(output_dir),
        str(input_path)
    ])

    # Return the path to the stems folder
    stems_folder = output_dir / DEFAULT_MODEL / input_path.stem
    return stems_folder