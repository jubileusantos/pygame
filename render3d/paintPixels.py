import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
from random import randint

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 6000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)

def drawText(text: str, pos: Vector2, fontSize: int=18, fontType: str="comicsans", bold: bool=False,
             italic: bool=False, antiAlias: bool=False, textColor: tuple=BLACK, bgColor: tuple=None,
             centerX: float=0, centerY: float=0, surface: pygame.Surface=window):
    font = pygame.font.SysFont(fontType, fontSize, bold, italic)
    textSurface = font.render(str(text), antiAlias, textColor, bgColor)
    textRect = textSurface.get_rect()
    surface.blit(textSurface, [pos.x + (textRect.width/2) * centerX, pos.y + (textRect.height/2) * centerY])

startX, endX = 100, 700
startY, endY = 100, 700
step = 2
size = 1

dt = 1000/FPS
paintPixels = True
while True:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    mousePos = Vector2(mouseX, mouseY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    window.fill(WHITE)

    points = []
    for x in range(startX, endX, step):
        for y in range(startY, endY, step):
            points.append((x, y))
            if not paintPixels:
                pygame.draw.circle(window, BLACK, (x, y), size)

    if paintPixels:
        for p in points:
            window.set_at(p, BLACK)

    drawText(f"FPS: {1000/dt:.0f}", Vector2(), fontSize=15)

    pygame.display.update()
    dt = clock.tick(FPS)