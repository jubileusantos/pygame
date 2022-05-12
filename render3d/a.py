import sys, pygame
from pygame.locals import *
import os.path
import math

pygame.init()
SCREEN = pygame.display.set_mode((800, 800))
CLOCK  = pygame.time.Clock()

w = 750
h = 150
surface = pygame.Surface((w, h), SRCALPHA)
image = pygame.image.load(os.path.join(__file__, "../connie.png"))
image = pygame.transform.scale(image, (w, h))
surface.fill((0, 0, 0))
surface.blit(image, (0, 0))
angle = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    SCREEN.fill((255, 255, 255))
    rotated_surface = pygame.transform.rotate(surface, math.sin(angle) * 25)
    rect = rotated_surface.get_rect(center = (400, 400))
    SCREEN.blit(rotated_surface, (rect.x, rect.y))

    angle += .1
    pygame.display.update()
    CLOCK.tick(30)

'''

TODO:
 - Aplicar rotação nas textureSurfaces de acordo com a rotação do cubo e GLOBAL_ROTATION

'''