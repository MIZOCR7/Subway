ZOMBIE HORDE — Free Top-Down Zombie Sprites, Blood FX & Zombie SFX
Arcade UI Forge   •   v1.0   •   FREE for commercial use

Eight animated top-down zombies (4 types x 2 color variants), a survivor
with a pistol, blood and gun FX, blood decals and 42 zombie, gore and
pistol sound effects. Everything a small zombie shooter or survival jam
game needs to get moving. The sprites and sounds are generated
procedurally with code.

CHARACTERS (32x32 frames, 3/4 top-down view)
  walker, walker_b      classic shambler
  runner, runner_b      hooded, lighter build
  brute, brute_b        big, bald, wide
  hazmat, hazmat_b      zombie in a hazmat suit
  survivor              player character with a pistol
  Every character has 4 directions (down, left, right, up) x
    idle (4 frames), walk (6), attack (5), hurt (2), death (6)
  = 92 frames each, 828 frames total. For the survivor, "attack" is a
  pistol shot with recoil and a muzzle flash.

  characters/<id>/frames/            every animation frame as its own PNG
  characters/<id>/meta.json          animation names, frame count, fps, loop
        Animation names use the animation and direction, e.g.
        walk_right_00.png. See PYTHON_GUIDE.md for a Pygame loader.

FX (fx/)
  blood_hit, blood_hit_right (32x32, 6 frames)
  blood_burst (48x48, 8 frames), gore_burst (64x64, 8 frames)
  muzzle_flash (16x16, 3 frames), bullet_impact (16x16, 4 frames)
  bullet.png, shell_casing.png (8x8)
  Individual animation frames are in fx/frames/.

DECALS (decals/)
  10 blood splatter decals (6 at 32x32, 4 at 16x16) for the floor.

SOUND EFFECTS (sfx/WAV and sfx/OGG, 44.1 kHz 16-bit stereo)
  zombie_voice     8 groans, 5 attack snarls, 4 hurt, 4 death gurgles
  zombie_movement  4 shuffling footsteps
  gore             5 flesh hits, 4 blood splats, 3 bites
  weapons          3 pistol shots, reload, empty click

manifest.json lists every character, FX strip, decal and sound.

ENGINES
  Works in Godot, Unity, GameMaker, Construct, Defold, Love2D or any
  engine that loads PNG + WAV/OGG. Use Nearest / Point filtering.
  Frames are 32x32 with the feet at the bottom center (y = 28).

WANT MORE?  Every paid Arcade UI Forge pack is 30% off this week
  (Black Friday Week Sale, through Nov 27):
  https://itch.io/s/222276/black-friday-week-sale
  • Barrow Brood — 28 animated top-down dungeon enemies
    https://arcadeuiforge.itch.io/barrow-brood
  • Satchel & Steel — 579 RPG item icons
    https://arcadeuiforge.itch.io/satchel-and-steel
  Store: https://arcadeuiforge.itch.io

LICENSE  Free for commercial and personal projects. Credit appreciated,
  not required. Don't resell or redistribute the pack itself.
  See LICENSE.txt.
