# Python asset layout

Use the individual PNGs in each `frames` folder as the canonical animation
format. Numbered filenames sort in playback order. Animation timing and loop
settings are in each character's `meta.json`.

```python
from assets.loader import load_frames

walk_right = load_frames("characters/survivor/frames", "walk_right")
hit_effect = load_frames("fx/frames", "blood_hit")
```

`load_frames` returns a list of Pygame surfaces and raises `FileNotFoundError`
if the requested animation is missing. Load frames after `pygame.init()`.

Other useful locations:

- `characters/<character>/frames/` — character animations
- `fx/frames/` — animated effects
- `decals/` — static blood decals
- `sfx/WAV/` — sound effects in WAV format
- `previews/` — pack preview; not needed by the game

The original license, asset manifest, and pack documentation are retained.
