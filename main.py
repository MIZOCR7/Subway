import pygame 
import sys 

pygame.init() 

WIDTH = 800
HEIGHT = 600 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption('Subway')  



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
    self.rect = pygame.Rect(self.x_pos, self.y_pos, 200, 100)
  
  
  def input(self):
    keys = [pygame.key.get_pressed()]
    
  
  
  def move(self):
    dx = 0 
    
    
    
    
  
  def draw(self):
    pygame.draw.rect(screen, (255, 0, 0), self.rect) 
    
  def update(self):
    self.draw()
    self.input() 


player = Player(20, 20) 


while True:
  screen.fill((0,0,0)) 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
      break
  
  player.update()
  
  pygame.display.update()
pygame.quit()
    
