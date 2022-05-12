from random import randint
import pygame
from pygame.locals import *
import sys
from math import radians, sin, cos, pi
from pygame.math import Vector2
from time import time

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PINK = (255, 127, 127)
PURPLE = (204, 51, 204)
CYAN = (127, 127, 255)

def map(n, start1, stop1, start2, stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2

class MovingBall:
    def __init__(self, lineStart: Vector2, lineEnd: Vector2, startBallAlpha: float=0, alphaOffset: float=0,
                 lineColor: tuple=BLACK, ballColor: tuple=WHITE, ballRadius: float=10, lineWidth: float=2) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.ballAlpha = startBallAlpha
        self.lineColor = lineColor
        self.ballColor = ballColor
        self.ballRadius = ballRadius
        self.lineWidth = lineWidth
        self.alphaOffset = alphaOffset

    def drawLine(self, surface: pygame.Surface=window) -> None:
        pygame.draw.line(surface, self.lineColor, self.lineStart, self.lineEnd, self.lineWidth)

    def drawBall(self, surface: pygame.Surface=window) -> None:
        pygame.draw.circle(surface, self.ballColor, self.lineStart.lerp(self.lineEnd, self.ballAlpha), self.ballRadius)

bgCircleRadius = 250
bgCircleColor = RED
bgCircleCenter = Vector2(WIDTH/2, HEIGHT/2)
lines = 256
movingBalls: list[MovingBall] = []
for i in range(lines):
    # Get angle and line start and end position
    angle = map(i, 0, lines, 0, 180)
    startX = bgCircleCenter.x + cos(radians(angle)) * bgCircleRadius
    startY = bgCircleCenter.y + sin(radians(angle)) * bgCircleRadius

    endX = bgCircleCenter.x + cos(radians(angle + 180)) * bgCircleRadius
    endY = bgCircleCenter.y + sin(radians(angle + 180)) * bgCircleRadius

    # Get alpha offset
    offset = pi/lines * i

    # Add to list
    movingBalls.append(MovingBall(Vector2(startX, startY), Vector2(endX, endY), alphaOffset=offset))

while True:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_e:
                # Add moving ball
                pass
            elif event.key == K_r and len(movingBalls) > 0:
                # Remove moving ball
                pass

    window.fill(BLACK)

    # Draw background circle
    pygame.draw.circle(window, bgCircleColor, bgCircleCenter, bgCircleRadius)

    # Calculate line drawing based on mouse pos
    idxEnd = map(mouseX, 0, WIDTH, 0, len(movingBalls))


    # Update alphas and draw lines
    for i in range(len(movingBalls)):
        if i > idxEnd:
            continue

        # Update ball alpha
        m = movingBalls[i]
        m.ballAlpha = map(sin(time() + m.alphaOffset), -1, 1, 0, 1)

        # Draw line
        m.drawLine()

    # Draw balls
    for i in range(len(movingBalls)):
        if i > idxEnd:
            continue

        m = movingBalls[i]
        m.drawBall()

    pygame.display.update()
    clock.tick(FPS)