import pygame 
import sys 
import os
import random
import glob
import math
from pygame.math import Vector2 as Vec

pygame.init() 

WIDTH = 800
HEIGHT = 600 
FPS = 960, 640, 60
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



class Character(pygame.sprite.Sprite):
  def __init__(self, x_pos, y_pos):
    super().__init__()
    self.x = x_pos
    self.y = y_pos 
    self.speed = 5
    self.is_alive = True  
  
  def update(self):
    pass 

class Player(Character):
  def __init__(self, x_pos, y_pos):
    super().__init__(x_pos, y_pos) 
    self.score = 0 
    self.x_pos = x_pos
    self.y_pos = y_pos 
    self.status = {'idle': False,
                   'right': False,
                   'left': False,
                   'shoot': False
                   } 
    self.image = pygame.image.load('assets/characters/survivor/frames/idle_down_00.png')  
    self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos)) 
    self.dx = 0
   
  def input(self):
    keys = pygame.key.get_pressed() 
    
    self.dx = 0
    self.status['right'] = False
    self.status['left'] = False 
    self.status['shoot'] = False  
    self.status['idle'] = False 
    
    
    if keys[pygame.K_a]: 
      self.status['left'] = True 
      self.dx = -self.speed
    elif keys[pygame.K_d]:
      self.status['right'] = True 
      self.dx = self.speed 
    else:
      self.status['idle'] = True
    
    if keys[pygame.K_SPACE]: 
      self.status['shoot'] = True 
    
    print(self.status)
  
  def move(self): 
    if self.status['right']:
      self.rect.x += self.dx
    elif self.status['left']:
      self.rect.x += self.dx 
    
    
  def draw(self):
    screen.blit(self.image, self.rect) 
    
  def update(self):
    self.draw()
    self.input() 
    self.move() 
  

player = Player(20, 20) 



def frames_loader(character, actions, direction):
  key = (character, tuple(actions), direction) 
  if key in _cache:
    return _cache[key] 
  
  folder = os.path.join(CHAR_DIR, character, 'frames') 
  files = []
  for action in actions:
    files = sorted(glob.glob(os.path.join(folder, f'{action}_{direction}_*.png'))) 
    if files:
      break
  if not files:
    files = sorted(glob.glob(os.path.join(folder, '*.png')))[:1] 
    
  frames = [] 
  for f in files:
    img = pygame.image.load(f).convert_alpha()
    w, h = img.get_size()
    frames.append(pygame.transform.scale(img, int(w * SPRITE_H / h), SPRITE_H))
    
  if not frames:
    surf = pygame.Surface((40, SPRITE_H)) 
    surf.fill((200, 50, 50)) 
    frames = [surf] 
    
  _cache[key] = frames
  return frames 

def dir_form_vec(v):
  if abs(v.x) > abs(v.y):
    return 'right' if v.x > 0 else 'left'
  return 'down' if v.y > 0 else 'up'


while True:
  clock.tick(FPS)
  screen.fill((0,0,0)) 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
      break
  
  player.update()
  
  pygame.display.update()
pygame.quit()
    
