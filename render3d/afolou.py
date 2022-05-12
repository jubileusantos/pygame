import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2, Vector3
from random import randint
from math import cos, pi, sin, radians, inf
from time import time
import rendering3d

rendering3d.orthographicProjection = False

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

faceColors = {
        "right": RED,
        "front": GREEN,
        "back": BLUE,
        "top": WHITE,
        "bottom": YELLOW,
        "left": ORANGE,
    }
afolouTextures = {
    "left": "afolou1.jpg",
    "right": "afolou2.jpg",
    "top": "afolou3.jpg",
    "bottom": "afolou4.jpeg",
    "back": "afolou5.jpeg",
    "front": "afolou6.jpg",
}

# Cria o cubo do a a folou
afolouCube = rendering3d.Cube(Vector3(WIDTH/2, HEIGHT/2, 1), 400, BLACK, edgeThickness=2, faceColors=faceColors, faceTextures=afolouTextures)

# Prepara a musiquita de fundo
pygame.mixer.init()
pygame.mixer.music.load("musica_afolou.mp3")
pygame.mixer.music.set_volume(15)
pygame.mixer.music.play(-1) # O primeiro argumento é o tanto de repetições da música; se for -1, repete infinitamente

while True:
    # Mouse input
    left, middle, right = pygame.mouse.get_pressed()
    leftButtonDown, rightButtonDown = left, right

    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    mousePos = Vector2(mouseX, mouseY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            if leftButtonDown:
                rendering3d.translate(event.rel[0], event.rel[1], 0)
            if rightButtonDown:
                rendering3d.rotate(event.rel[1], event.rel[0], 0)

    window.fill(WHITE)

    afolouCube.draw(drawTextures=True)

    pygame.display.set_caption(f"A a folou | FPS: {clock.get_fps():.0f}")
    pygame.display.update()
    clock.tick(FPS)