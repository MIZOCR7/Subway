# Subway

Welcome to **Subway**, U are the last survivor at a dark subway, and zombies keep coming from every side. Shoot them, don't let them touch you, and see how high your score can get.

## Description

I built this game with **pure Python and Pygame**, without any heavy game engine like Unity or Godot. Movement, aiming, shooting, zombie chasing, collisions, animations, sounds and the blood on the floor are all written in code.

### Features

- Move with the keyboard and aim with the mouse
- Zombies spawn from all 4 sides and chase you
- Different zombies: slow walkers, fast runners, and tough hazmat zombies that take 3 hits
- Every character has its own animations: idle, walk, attack, hurt and death, in 4 directions
- Blood stays on the floor after every hit
- Pistol with a magazine, empty click and reload
- Zombie groans, footsteps, bites and gunshots, quieter when far away
- The game gets harder as your score grows

### Controls

| Key | Action |
| --- | --- |
| W A S D | Move |
| Mouse | Aim |
| Left click / Space | Shoot |
| R | Reload (and restart after game over) |

## Things you might want to read

- Characters (survivor and zombies): **https://arcadeuiforge.itch.io/zombie-horde?download**

### Screenshots

<img width="955" height="667" alt="Screenshot 2026-11-22 125636" src="https://github.com/user-attachments/assets/3d263134-6ecd-4af4-8497-375f2a24d866" />
<img width="960" height="670" alt="Screenshot 2026-11-22 125624" src="https://github.com/user-attachments/assets/831b5afe-6f29-4e80-b722-c309ccb5c22b" />

## Getting Started

### Dependencies

- Python 3.10 or newer installed on your system
- Pygame library

### Installing

<!-- Delete this section if you did not make a release (a downloadable .exe) -->
Windows: **https://github.com/MIZOCR7/Subway/releases/tag/v1**

### Executing program

You can play the game in one of two ways:

### Option 1: Quick Play (No Setup Required)
1. Download the standalone executable (`.exe`) from the Releases page of this repository.
2. Double-click the file to launch the game instantly. No Python or extra dependencies needed!

### Option 2: Run from Source Code
If you prefer to run the raw code, follow these steps in your terminal or PowerShell:

1. Clone the repository:
   ```bash
   git clone https://github.com/MIZOCR7/Subway
   ```
2. Go into the folder:
   ```bash
   cd Subway
   ```
3. Install Pygame (use `pip3` if you have Mac or Linux, and `pip` if you have Windows):
   ```bash
   pip install pygame
   ```
4. Run the game from the code directly:
   ```bash
   python main.py
   ```

> Important: run the game from inside the `Subway` folder, because `main.py` looks for the `assets` folder next to it.

### Project structure

```text
Subway/
├── main.py          # the whole game
└── assets/
    ├── characters/  # survivor and zombie animation frames
    ├── decals/      # blood decals
    ├── fx/          # effects
    └── sfx/         # sounds
```

`background.png` can be anywhere inside the project folder, the game will find it.

## Have fun

If you like the game, give it a star on GitHub!
