import pygame 
import sys 
import os
import random
import glob
import math
from pygame.math import Vector2 as Vec 
from assets.loader import load_frames as load_asset_frames

pygame.init() 

WIDTH, HEIGHT, FPS = 960, 640, 60
SPRITE_H = 72 
SIDEWALK_H = 64 
ATTACK_RANGE = 40 
MAX_ENEMIES = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption('Subway')  
clock = pygame.time.Clock() 

font = pygame.font.SysFont('consolas', 28)
big_font = pygame.font.SysFont('consolas', 64)
pygame.mouse.set_visible(False)

BASE = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(BASE, 'assets', 'background.jpg')
CHAR_DIR = os.path.join(BASE, 'assets', 'characters')
DECAL_DIR = os.path.join(BASE, 'assets', 'decals')
SFX_DIR = os.path.join(BASE, 'assets', 'sfx', 'WAV')

MAG_SIZE = 12         
RELOAD_TIME = 1.2

ZOMBIES = {
  'walker':   (70, 1, 10),
  'walker_b': (80, 1, 10),
  'runner':   (150, 1, 15),
  'runner_b': (170, 1, 15),
  'hazmat_b': (60, 3, 30),
}
SPAWN_WEIGHTS = {'walker': 4, 'walker_b': 4, 'runner': 2, 'runner_b': 2, 'hazmat_b': 1}

_cache = {}


def load_frames(character, actions, direction):
  key = (character, tuple(actions), direction)
  if key not in _cache:
    for action in actions:
      try:
        frames = load_asset_frames(
          os.path.join('characters', character, 'frames'),
          f'{action}_{direction}'
        )
        _cache[key] = [
          pygame.transform.scale(frame, (int(frame.get_width() * SPRITE_H / frame.get_height()), SPRITE_H))
          for frame in frames
        ]
        break
      except FileNotFoundError:
        continue
    else:
      raise FileNotFoundError(f'No {actions} frames for {character} facing {direction}')
  return _cache[key]


def dir_from_vec(vector):
  if abs(vector.x) > abs(vector.y):
    return 'right' if vector.x > 0 else 'left'
  return 'down' if vector.y > 0 else 'up'


try:
  pygame.mixer.set_num_channels(32)
except pygame.error:
  pass


def load_sounds(folder, prefix):
  if not pygame.mixer.get_init():
    return []
  sounds = []
  for path in sorted(glob.glob(os.path.join(SFX_DIR, folder, prefix + '*.wav'))):
    try:
      sounds.append(pygame.mixer.Sound(path))
    except pygame.error:
      pass
  return sounds


SFX = {
  'shot': load_sounds('weapons', 'pistol_shot'),
  'empty': load_sounds('weapons', 'pistol_empty'),
  'reload': load_sounds('weapons', 'pistol_reload'),
  'flesh': load_sounds('gore', 'flesh_hit'),
  'splat': load_sounds('gore', 'blood_splat'),
  'bite': load_sounds('gore', 'zombie_bite'),
  'step': load_sounds('zombie_movement', 'zombie_footstep'),
  'zdeath': load_sounds('zombie_voice', 'zombie_death'),
  'groan': load_sounds('zombie_voice', 'zombie_groan'),
  'zhurt': load_sounds('zombie_voice', 'zombie_hurt'),
  'snarl': load_sounds('zombie_voice', 'zombie_snarl'),
}


def play(name, volume=1.0):
  sounds = SFX.get(name)
  if sounds and volume > 0.02:
    channel = random.choice(sounds).play()
    if channel:
      channel.set_volume(min(1.0, volume))




def load_background():
  img = pygame.image.load(BG_PATH).convert_alpha()
  w, h = img.get_size() 
  scale = max(WIDTH / w, HEIGHT / h)
  img = pygame.transform.scale(img, (int(w * scale) + 1, int(h * scale)+ 1))
  surf = pygame.Surface((WIDTH, HEIGHT))
  surf.blit(img, ((WIDTH - img.get_width()) // 2, (HEIGHT - img.get_height()) // 2)) 
  return surf 


def make_floor():
  return load_background()


def load_blood():
  files = [f for f in glob.glob(os.path.join(DECAL_DIR, '*.png'))
           if 'blood' in os.path.basename(f).lower()] 
  imgs = [pygame.image.load(f).convert_alpha() for f in files] 
  return imgs


blood_imgs = load_blood()
floor = make_floor()


def stamp_blood(pos, scale=1.0):
  img = random.choice(blood_imgs)
  w, h = img.get_size()
  img = pygame.transform.scale(img, (max(4, int(w * scale)), max(4, int(h * scale)))) 
  img = pygame.transform.rotate(img, random.randint(0, 359))
  floor.blit(img, img.get_rect(center=(round(pos.x), round(pos.y))))


class Animated:
  def __init__(self, pos):
    super().__init__()
    self.pos = Vec(pos) 
    self.frames = []
    self.index = 0.0
    self.loop = True 
    self.finished = False 
    
  def set_anim(self, frames, loop=True):
    if frames is not self.frames:
      self.frames = frames
      self.index = 0.0
      self.loop = loop
      self.finished = False 
      
  def animate(self, dt, anim_fps=10):
    self.index += anim_fps * dt
    if self.loop:
      self.index %= len(self.frames)
    elif self.index >= len(self.frames):
      self.index = len(self.frames) - 1  
      self.finished = True
    self.image = self.frames[int(self.index)]
    self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y))) 

  def draw(self, surface):
    surface.blit(self.image, self.rect) 
  

class Bullet:
  SPEED = 800 
  
  def __init__(self, pos, direction):
    self.pos = Vec(pos)
    self.vel = direction * self.SPEED
    self.alive =  True 
  
  def update(self, dt): 
    self.pos += self.vel * dt
    if not (-20 < self.pos.x < WIDTH + 20 and -20 < self.pos.y < HEIGHT + 20):
      self.alive = False 
  
  def draw(self, surface):
    tail = self.pos - self.vel.normalize() * 12
    pygame.draw.line(surface, (255, 255, 90), tail, self.pos, 3) 


class Player(Animated):
  def __init__(self, x, y):
    super().__init__((x, y)) 
    self.speed = 220
    self.hp = 5
    self.score = 0
    self.facing = 'down'
    self.aim = Vec(0, 1) 
    self.shoot_cooldown = 0.0 
    self.hurt_timer = 0.0
    self.dead = False 
    self.moving = False 
    self.ammo = MAG_SIZE
    self.reload_timer = 0.0
    self.reload_delay = 0.0
    self.empty_cd = 0.0
    
    self.frames = load_frames('survivor', ['idle'], 'down')
    self.animate(0) 
    
  def hit(self):
    self.hp -= 1
    self.hurt_timer = 1.0
    
    if self.hp <= 0:
      self.dead = True 
  
  def start_reload(self):
    self.reload_timer = RELOAD_TIME

    play('reload', 0.7)

  def anim(self, action, loop=True):
    self.set_anim(load_frames('survivor', [action, 'idle'], self.facing), loop)

  def update(self, dt, bullets):
    if self.dead:
      self.anim('death', loop=False)
      self.animate(dt)
      return

    keys = pygame.key.get_pressed()
    move = Vec(keys[pygame.K_d] - keys[pygame.K_a],
               keys[pygame.K_s] - keys[pygame.K_w])
    self.moving = move.length_squared() > 0
    if self.moving:
      self.pos += move.normalize() * self.speed * dt
    self.pos.x = max(20, min(WIDTH - 20, self.pos.x))
    self.pos.y = max(20, min(HEIGHT - 20, self.pos.y))

    to_mouse = Vec(pygame.mouse.get_pos()) - self.pos
    if to_mouse.length() > 8:
      self.aim = to_mouse.normalize()
      self.facing = dir_from_vec(to_mouse)

    shooting = pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]
    if self.hurt_timer > 0.7:
      self.anim('hurt', loop=False)
    elif shooting:
      self.anim('attack')
    elif self.moving:
      self.anim('walk')
    else:
      self.anim('idle')
    self.animate(dt)
    self.shoot_cooldown -= dt
    self.empty_cd -= dt

    if self.reload_delay > 0:
      self.reload_delay -= dt
      if self.reload_delay <= 0:
        self.start_reload()
    if self.reload_timer > 0:
      self.reload_timer -= dt
      if self.reload_timer <= 0:
        self.ammo = MAG_SIZE
    elif keys[pygame.K_r] and self.ammo < MAG_SIZE and self.reload_delay <= 0:
      self.start_reload()

    if shooting and self.shoot_cooldown <= 0 and self.reload_timer <= 0:
      if self.ammo > 0:
        bullets.append(Bullet(self.pos + self.aim * 30, self.aim))
        self.ammo -= 1
        self.shoot_cooldown = 0.2
        play('shot', 0.5)
      elif self.empty_cd <= 0 and self.reload_delay <= 0:
        play('empty', 0.7)
        self.empty_cd = 0.4
        self.reload_delay = 0.35
    self.hurt_timer -= dt

  def draw(self, surface):
    if not self.dead and 0 < self.hurt_timer <= 0.7 and int(self.hurt_timer * 15) % 2 == 0:
      return
    super().draw(surface)


class Zombie(Animated):
  def __init__(self, kind):
    side = random.choice('tblr')
    if side == 't':
      pos = (random.randint(0, WIDTH), -40)
    elif side == 'b':
      pos = (random.randint(0, WIDTH), HEIGHT + 40)
    elif side == 'l':
      pos = (-40, random.randint(0, HEIGHT))
    else:
      pos = (WIDTH + 40, random.randint(0, HEIGHT))
    super().__init__(pos)
    self.kind = kind
    speed, self.hp, self.points = ZOMBIES[kind]
    self.speed = speed * random.uniform(0.9, 1.15)
    self.facing = 'down'
    self.dying = False
    self.alive = True
    self.hurt_timer = 0.0
    self.attack_cd = 0.0
    self.groan_timer = random.uniform(2, 8)
    self.step_timer = random.uniform(0, 0.6)
    self.frames = load_frames(kind, ['walk'], 'down')
    self.animate(0)

  def anim(self, action, loop=True):
    self.set_anim(load_frames(self.kind, [action, 'idle'], self.facing), loop)

  def hit(self):
    self.hp -= 1
    play('flesh', 0.7)
    if self.hp <= 0:
      self.dying = True
      self.anim('death', loop=False)
      stamp_blood(self.pos, random.uniform(0.9, 1.4))
      play('zdeath', 0.8)
      play('splat', 0.6)
      return True
    self.hurt_timer = 0.2
    play('zhurt', 0.6)
    if random.random() < 0.6:
      stamp_blood(self.pos, 0.4)
    return False

  def update(self, dt, player, zombies):
    if self.dying:
      self.animate(dt)
      if self.finished:
        self.alive = False
      return

    to_player = player.pos - self.pos
    distance = to_player.length()
    if distance > 1:
      self.facing = dir_from_vec(to_player)
    direction = to_player / distance if distance > 1 else Vec()
    self.hurt_timer -= dt
    self.attack_cd -= dt

    if player.dead:
      action, speed_mult = 'idle', 0
    elif self.hurt_timer > 0:
      action, speed_mult = 'hurt', 0.3
    elif distance < ATTACK_RANGE:
      action, speed_mult = 'attack', 0
      if self.attack_cd <= 0 and player.hurt_timer <= 0:
        player.hit()
        play('snarl', 0.7)
        play('bite', 0.9)
        self.attack_cd = 0.8
    else:
      action, speed_mult = 'walk', 1

    if speed_mult:
      velocity = direction * self.speed * speed_mult
      for other in zombies:
        if other is not self and not other.dying:
          separation = self.pos - other.pos
          if 0 < separation.length() < 28:
            velocity += separation.normalize() * 60
      self.pos += velocity * dt

    closeness = max(0, 1 - distance / 450)
    self.groan_timer -= dt
    if self.groan_timer <= 0:
      play('groan', 0.7 * closeness)
      self.groan_timer = random.uniform(4, 9)
    if action == 'walk' and distance < 350:
      self.step_timer -= dt
      if self.step_timer <= 0:
        play('step', 0.35 * closeness)
        self.step_timer = random.uniform(0.45, 0.7)

    self.anim(action, loop=action != 'hurt')
    self.animate(dt)


def reset():
  global floor
  floor = make_floor()
  return Player(WIDTH // 2, HEIGHT // 2), [], []


def draw_crosshair(pos):
  x, y = pos
  pygame.draw.circle(screen, (255, 255, 255), (x, y), 10, 1)
  pygame.draw.line(screen, (255, 255, 255), (x - 16, y), (x - 6, y), 1)
  pygame.draw.line(screen, (255, 255, 255), (x + 6, y), (x + 16, y), 1)
  pygame.draw.line(screen, (255, 255, 255), (x, y - 16), (x, y - 6), 1)
  pygame.draw.line(screen, (255, 255, 255), (x, y + 6), (x, y + 16), 1)


player, bullets, zombies = reset()
spawn_timer = 1.0

while True:
  dt = min(clock.tick(FPS) / 1000, 0.05)
  game_over = player.dead and player.finished
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
      player, bullets, zombies = reset()
      spawn_timer = 1.0

  if not player.dead:
    spawn_timer -= dt
    if spawn_timer <= 0 and len(zombies) < MAX_ENEMIES:
      kind = random.choices(list(SPAWN_WEIGHTS), list(SPAWN_WEIGHTS.values()))[0]
      zombies.append(Zombie(kind))
      spawn_timer = max(0.3, 1.5 - player.score / 400)

  player.update(dt, bullets)
  for bullet in bullets:
    bullet.update(dt)
  for zombie in zombies:
    zombie.update(dt, player, zombies)
  for bullet in bullets:
    for zombie in zombies:
      if not zombie.dying and (bullet.pos - zombie.pos).length_squared() < 22 ** 2:
        bullet.alive = False
        if zombie.hit():
          player.score += zombie.points
        break

  bullets = [bullet for bullet in bullets if bullet.alive]
  zombies = [zombie for zombie in zombies if zombie.alive]
  screen.blit(floor, (0, 0))
  for zombie in zombies:
    if zombie.dying:
      zombie.draw(screen)
  living = [zombie for zombie in zombies if not zombie.dying] + [player]
  for sprite in sorted(living, key=lambda item: item.pos.y):
    sprite.draw(screen)
  for bullet in bullets:
    bullet.draw(screen)

  screen.blit(font.render(f'Score: {player.score}', True, (255, 255, 255)), (15, 12))
  screen.blit(font.render(f'HP: {max(player.hp, 0)}', True, (255, 90, 90)), (15, 44))
  ammo = 'RELOADING...' if player.reload_timer > 0 else f'Ammo: {player.ammo}/{MAG_SIZE}'
  screen.blit(font.render(ammo, True, (255, 225, 90)), (15, 76))
  draw_crosshair(pygame.mouse.get_pos())

  if game_over:
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 150))
    screen.blit(shade, (0, 0))
    title = big_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    hint = font.render('Press R to restart', True, (210, 210, 210))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

  pygame.display.update()
  