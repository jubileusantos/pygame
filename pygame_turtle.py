import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
from math import sin, cos, radians, degrees, atan2
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

class Turtle:
    def __init__(self, pos: Vector2, angle: float=0, radius=25, color=BLACK) -> None:
        self.pos = pos
        self.color = color
        self.angle = angle
        self.radius = radius
        self.trail = []

    def color(self, color):
        self.color = color
    
    def forward(self, amount):
        self.pos.x += cos(radians(self.angle)) * amount
        self.pos.y += sin(radians(self.angle)) * amount

    def turnLeft(self, angle):
        self.angle -= angle

    def turnRight(self, angle):
        self.angle += angle

    def calcPos(self, walk):
        x = self.pos.x + cos(radians(self.angle)) * walk
        y = self.pos.y + sin(radians(self.angle)) * walk

        return Vector2(x, y)

    def setPos(self, x: float, y: float):
        self.pos.x = x
        self.pos.y = y

    def setAngle(self, angle: float):
        self.angle = angle

    def draw(self, surface=window):
        # Draw trail
        for i in range(len(self.trail)-1):
            color = pygame.Color(0, 0, 0)
            color.hsla = ((i/len(self.trail)-1 * 1) % (i+1) % 360, 100, 50, 100)
            p1 = self.trail[i]
            p2 = self.trail[i+1]
            a = 35
            r = 0
            pygame.draw.line(surface, self.color, (p1[0] + cos(frame/randint(15,35)) * r, p1[1] + sin(frame/randint(15,35)) * r), (p2[0] + cos(frame/randint(15,35)) * r, p2[1] + sin(frame/randint(15,35)) * r), 2)

        self.trail.append((self.pos.x, self.pos.y))

        x = self.pos.x + cos(radians(self.angle)) * self.radius
        y = self.pos.y + sin(radians(self.angle)) * self.radius
        pygame.draw.circle(surface, self.color, (self.pos.x, self.pos.y), self.radius)
        pygame.draw.line(surface, RED, (self.pos.x, self.pos.y), (x, y), 2)

def map(n, start1, stop1, start2, stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2

def calcPoints(t: Turtle, n: int, angle: float, walkA: float, inc: float=1, left=True):
    points = []

    origX = t.pos.x
    origY = t.pos.y
    origA = t.angle
    for i in range(n):
        points.append(t.calcPos(walkA))
        if left:
            t.turnLeft(angle)
        else:
            t.turnRight(angle)

        t.forward(walkA + inc*i)

    t.setPos(origX, origY)
    t.setAngle(origA)
    return points

center = Vector2(WIDTH/2, HEIGHT/2)
t = Turtle((center), radius=3, color=BLACK)
a = 1
angleR = 150
frame = 0

while True:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    window.fill(WHITE)

    # Calculate color
    direction = Vector2(mouseX, mouseY) - center
    try:
        directionUnit = direction.normalize()
    except ValueError:
        continue
    angle = degrees(atan2(direction.y, direction.x))
    color = pygame.Color(0, 0, 0)
    color.hsla = ((angle + 90) % 360, 100, map(direction.magnitude(), 0, max(WIDTH, HEIGHT), 100, 0), 0)
    
    #mouseX = WIDTH/2
    #mouseY = HEIGHT/2
    points = calcPoints(t, int(map(mouseX, 0, WIDTH, 0, 3000)), map(mouseY, 0, HEIGHT, 0, 180), 1, .2)
    for i in range(len(points)-1):
        p1 = points[i]
        p2 = points[i+1]

        pygame.draw.line(window, color, (p1[0], p1[1]), (p2[0], p2[1]), 2)
    
    # Show angle
    pygame.draw.circle(window, BLACK, (WIDTH/2, HEIGHT/2), direction.magnitude(), 3)
    pygame.draw.line(window, RED, (WIDTH/2, HEIGHT/2), (WIDTH/2 + cos(radians(angle)) * direction.magnitude(), HEIGHT/2 + sin(radians(angle)) * direction.magnitude()))

    pygame.display.update()
    frame += 1
    clock.tick(FPS)