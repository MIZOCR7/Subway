import pygame 

pygame.init() 

WIDTH = 800
HEIGHT = 600 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption('Subway') 


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      
      break
    
