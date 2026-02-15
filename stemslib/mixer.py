from pathlib import Path
import torchaudio
from .utils import STEM_NAMES, DEFAULT_EXCLUDE

def mix_stems(stems_folder, exclude=None, output_path=None):
    """
    Recombine separated stems into a single mix, excluding specified instruments.
    
    Args:
        stems_folder (str): Path to the folder containing separated stems.
        exclude (list): List of stem names to exclude (e.g., ["guitar"]).
        output_path (str): Path to save the mixed audio file. If None, auto-generated.
    """
    stems_folder = Path(stems_folder).resolve()
    
    if not stems_folder.exists() or not stems_folder.is_dir():
        raise FileNotFoundError(f"Stems folder not found: {stems_folder}")
    
    if exclude is None:
        exclude = DEFAULT_EXCLUDE

    if output_path is None:
        exclude_str = "_".join(sorted(exclude))
        output_path = stems_folder / f"no_{exclude_str}.wav"
    else:
        output_path = Path(output_path)
    
    # Validate exclude list
    for stem in exclude:
        if stem not in STEM_NAMES:
            raise ValueError(f"Invalid stem name in exclude list: {stem}. Valid options: {STEM_NAMES}")
    
    # Load and sum the included stems
    mix = None
    sample_rate = None
    stems_to_mix = [s for s in STEM_NAMES if s not in exclude]
    
    for stem_name in stems_to_mix:
        stem_file = stems_folder / f"{stem_name}.wav"
        
        if not stem_file.exists():
            print(f"  Warning: Stem file not found, skipping: {stem_file}")
            continue
        
        audio, sr = torchaudio.load(str(stem_file))
        
        if sample_rate is None:
            sample_rate = sr
        
        if mix is None:
            mix = audio
        else:
            mix += audio
    
    if mix is None:
        raise RuntimeError("No valid stems found to mix.")
    
    torchaudio.save(str(output_path), mix, sample_rate)
    return output_path