import pygame
from pygame.locals import *
import sys
import os.path
from pygame import Vector2

WIDTH = 800
HEIGHT = 800
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Image
image = pygame.image.load(os.path.join(__file__, "../connie.png")).convert_alpha()
points = [
    Vector2(187, 159),
    Vector2(672, 203),
    Vector2(574, 645),
    Vector2(256, 534)
]

frame = 0
while True:
    mouseX, mouseY = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

    window.fill('grey')

    minX, maxX = WIDTH, 0
    minY, maxY = HEIGHT, 0
    for point in points:
        if point.x > maxX:
            maxX = point.x
        if point.x < minX:
            minX = point.x
        if point.y > maxY:
            maxY = point.y
        if point.y < minY:
            minY = point.y
    
    size = Vector2(maxX - minX, maxY - minY)

    # Draw image
    image = pygame.transform.scale(image, size)

    # Draw polygon
    polygonSurf = pygame.Surface(size, BLEND_RGBA_MAX).convert_alpha()
    polygonSurf.fill((255, 255, 255, 0))

    # Polygon mask
    polygonRect = pygame.draw.polygon(polygonSurf, BLACK, [(point.x - minX, point.y - minY) for point in points])
    polygonMask = pygame.mask.from_surface(polygonSurf)
    polygonMask.invert()
    newPolygonSurf = polygonMask.to_surface()
    newPolygonSurf.set_colorkey(BLACK)
    
    # Draw surfaces
    window.blit(image, (minX, minY))
    # window.blit(polygonSurf, (minX, minY))
    window.blit(newPolygonSurf, (minX, minY))
    frame += 1
    pygame.display.update()