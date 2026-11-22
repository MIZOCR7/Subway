from pathlib import Path
from typing import List

import pygame


ASSET_DIR = Path(__file__).resolve().parent


def load_frames(folder: str, animation: str) -> List[pygame.Surface]:
    """Load numbered PNG frames from a folder in animation order."""
    frame_dir = ASSET_DIR / folder
    prefix = f"{animation}_"
    paths = [
        path for path in frame_dir.glob(f"{prefix}*.png")
        if path.stem[len(prefix):].isdigit()
    ]
    paths.sort(key=lambda path: int(path.stem[len(prefix):]))
    if not paths:
        raise FileNotFoundError(
            f"No frames found for {animation!r} in {frame_dir}"
        )
    return [pygame.image.load(str(path)) for path in paths]
