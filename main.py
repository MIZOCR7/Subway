import pygame 
import sys 

pygame.init() 

WIDTH = 800
HEIGHT = 600 
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption('Subway')  
clock = pygame.time.Clock()



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
    self.y_pos = x_pos 
    self.status = {'idle': False,
                   'right': False,
                   'left': False,
                   'shoot': False
                   } 
    self.rect = pygame.Rect(self.x_pos, self.y_pos, 200, 100)
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
    pygame.draw.rect(screen, (255, 0, 0), self.rect) 
    
  def update(self):
    self.draw()
    self.input() 
    self.move() 
  

player = Player(20, 20) 


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
    
