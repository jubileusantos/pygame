import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
import math
import numpy
from random import randint

pygame.init()
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

def clamp(n: float, minVal: float, maxVal: float) -> float:
    return min(maxVal, max(minVal, n))

def drawText(text: str, pos: Vector2, fontSize: int=18, fontType: str="comicsans", bold: bool=False,
             italic: bool=False, antiAlias: bool=False, textColor: tuple=BLACK, bgColor: tuple=None,
             centerX: float=0, centerY: float=0, surface: pygame.Surface=window):
    font = pygame.font.SysFont(fontType, fontSize, bold, italic)
    textSurface = font.render(text, antiAlias, textColor, bgColor)
    textRect = textSurface.get_rect()
    surface.blit(textSurface, [pos.x + (textRect.width/2) * centerX, pos.y + (textRect.height/2) * centerY])

class Brick:
    def __init__(self, pos: Vector2, size: Vector2, health: int=1, color: tuple=BLACK, textureFile: str=None, isMovePad: bool=False) -> None:
        self.pos = pos
        self.width = size.x
        self.height = size.y
        self.color = color
        self.textureFile = textureFile
        self.maxHealth = health
        self.health = self.maxHealth
        self.isMovePad = isMovePad

    def draw(self, surface: pygame.Surface=window, drawOutline: bool=True) -> None:
        if self.textureFile:
            # Load texture
            pass
        else:
            # Draw the rect
            pygame.draw.rect(surface, self.color, (self.pos.x - self.width/2, self.pos.y - self.height/2, self.width, self.height))
            
            # Draw outlines
            if drawOutline:
                pygame.draw.rect(surface, brickOutlineColor, (self.pos.x - self.width/2, self.pos.y - self.height/2, self.width, self.height), brickOutlineWidth)

            # Draw the brick current health
            if not self.isMovePad and debugMode:
                drawText(str(self.health), self.pos, bold=True, textColor=GREEN, centerX=-1, centerY=-1, surface=surface)

class Ball:
    def __init__(self, pos: Vector2, vel: Vector2, speed: float=3, radius: int=15, color: tuple=RED) -> None:
        self.pos = pos
        self.vel = vel.normalize()
        self.color = color
        self.radius = radius
        self.speed = speed
    
    def update(self) -> bool:
        if self.vel.x == 0:
            self.vel.x += .1
        if self.vel.y == 0:
            self.vel.y += .1
        # Calculate next position
        targetPos = self.pos + self.vel.normalize() * self.speed * speedMult

        if targetPos.y > HEIGHT - self.radius:
            # Eliminate this ball
            return True

        # Collision with borders
        if targetPos.x < self.radius or targetPos.x > WIDTH - self.radius:
            self.vel.x *= -1
        if targetPos.y < self.radius or targetPos.y > HEIGHT - self.radius:
            self.vel.y *= -1

        # Get the smallest possible area to check collisions for performance
        areaTL = Vector2(0, 0)
        areaTL.x = min(self.pos.x, targetPos.x)
        areaTL.y = min(self.pos.y, targetPos.y)
        areaTL -= Vector2(self.radius, self.radius) * 2
        areaTL.x = max(areaTL.x, 0)
        areaTL.y = max(areaTL.y, 0)
        areaBR = Vector2(0, 0)
        areaBR.x = max(self.pos.x, targetPos.x)
        areaBR.y = max(self.pos.y, targetPos.y)
        areaBR += Vector2(self.radius, self.radius) * 2
        areaBR.x = min(areaBR.x, WIDTH)
        areaBR.y = min(areaBR.y, HEIGHT)

        # Check collision for all bricks in the calculated area
        for brick in bricks + [movePad]:
            if clamp(brick.pos.x, areaTL.x - brick.width/2, areaBR.x + brick.width/2) == brick.pos.x and clamp(brick.pos.y, areaTL.y - brick.height/2, areaBR.y + brick.height/2) == brick.pos.y:
                # Calculate
                nearestPoint = Vector2()
                nearestPoint.x = max(brick.pos.x - brick.width/2, min(targetPos.x, brick.pos.x + brick.width/2))
                nearestPoint.y = max(brick.pos.y - brick.height/2, min(targetPos.y, brick.pos.y + brick.height/2))

                rayToNearest = nearestPoint - targetPos
                try:
                    overlap = self.radius  - rayToNearest.magnitude()
                except ZeroDivisionError:
                    overlap = 0

                if overlap > 0:
                    brick.health -= 1
                    try:
                        normalized = rayToNearest.normalize()
                    except ValueError:
                        normalized = rayToNearest

                    # Adjust velocity when the rotation degree is horizontal or vertical
                    deg = math.degrees(math.atan2(normalized.y, normalized.x))
                    if abs(deg - 90) < .1 or abs(deg + 90) < .1:
                        # Calculate normal of face and reflect
                        if abs(nearestPoint.y - brick.pos.y - brick.height/2) < .1:
                            # Right wall
                            # Calculate normal of left/right wall
                            start = Vector2(brick.pos.x - brick.width/2, brick.pos.y - brick.height/2)
                            end = Vector2(brick.pos.x + brick.width/2, brick.pos.y - brick.height/2)
                            direc = (end - start).normalize()
                            normal = Vector2(-direc.y, direc.x)
                            self.vel.reflect_ip(normal)
                        elif abs(nearestPoint.y - brick.pos.y + brick.height/2) < .1:
                            # Left wall
                            start = Vector2(brick.pos.x - brick.width/2, brick.pos.y + brick.height/2)
                            end = Vector2(brick.pos.x + brick.width/2, brick.pos.y + brick.height/2)
                            direc = (end - start).normalize()
                            normal = Vector2(-direc.y, direc.x)
                            self.vel.reflect_ip(normal)
                    elif abs(deg - 180) < .1 or deg < .1:
                        if abs(nearestPoint.x - brick.pos.x - brick.width/2) < .1:
                            # Right wall
                            # Calculate normal of right wall
                            start = Vector2(brick.pos.x - brick.width/2, brick.pos.y - brick.height/2)
                            end = Vector2(brick.pos.x - brick.width/2, brick.pos.y + brick.height/2)
                            direc = (end - start).normalize()
                            normal = Vector2(-direc.y, direc.x)
                            self.vel.reflect_ip(normal)
                        elif abs(nearestPoint.x - brick.pos.x + brick.width/2) < .1:
                            # Left wall
                            start = Vector2(brick.pos.x + brick.width/2, brick.pos.y - brick.height/2)
                            end = Vector2(brick.pos.x + brick.width/2, brick.pos.y + brick.height/2)
                            direc = (end - start).normalize()
                            normal = Vector2(-direc.y, direc.x)
                            self.vel.reflect_ip(normal)
                    else:
                        self.vel = -normalized

                    #self.vel = -normalized
                    targetPos = targetPos - normalized * overlap

        if debugMode:
            pygame.draw.rect(window, GREEN, (areaTL.x, areaTL.y, areaBR.x - areaTL.x, areaBR.y - areaTL.y), 0)

        # Update position
        targetPos.x = clamp(targetPos.x, self.radius + 1, WIDTH - self.radius - 1)
        targetPos.y = clamp(targetPos.y, self.radius + 1, HEIGHT - self.radius - 1)
        self.pos = self.pos + self.vel * self.speed * speedMult

        return False

    def draw(self, surface: pygame.Surface=window) -> None:
        pygame.draw.circle(surface, self.color, (self.pos.x, self.pos.y), self.radius)

# States
debugMode = False
movementWithKeyboard = True
generateFullLevel = False
generateRandomLevel = True
brickChance = .4

# Move Pad
movePadGroundDistance = 50
movePadW = 80
movePadH = 15
movePad = Brick(Vector2(WIDTH/2, HEIGHT - movePadGroundDistance), Vector2(movePadW, movePadH), color=BLACK, isMovePad=True)
moveSpeed = 3
xMove = 0

# Bricks info
brickCols = 10
brickRows = 10
maxBrickYpos = HEIGHT/2
brickW = WIDTH / brickCols
brickH = maxBrickYpos / brickRows

# Levels Configuration
bricks: list[Brick] = []
brickOutlineColor = (0, 255, 255)
brickOutlineWidth = 1
brickChar = "#"
level1 = [
    '##########',
    '#........#',
    '#..#..#..#',
    '#..#..#..#',
    '#........#',
    '#.#....#.#',
    '#..#..#..#',
    '#...##...#',
    '#........#',
    '##########',
]
level2 = [
    '##########',
    '#........#',
    '#..#..#..#',
    '#..#..#..#',
    '#........#',
    '#...##...#',
    '#..#..#..#',
    '#.#....#.#',
    '#........#',
    '##########',
]
level3 = [
    '..........',
    '....##....',
    '...#..#...',
    '...#..#...',
    '...#..#...',
    '...#..#...',
    '..#....#..',
    '.#..##..#.',
    '..##..##..',
    '..........',
]
chosenMap = level3

# Setup level
for i in range(brickCols):
    for j in range(brickRows):

        # Get the char from the bricks map
        try:
            char = chosenMap[j][i]
        # If out of bounds, just don't do anything
        except IndexError:
            char = brickChar*2
        if (not generateRandomLevel and (char == brickChar or generateFullLevel)) or (generateRandomLevel and randint(0, 1000)/1000 < brickChance):
            x = WIDTH/brickCols * i
            y = maxBrickYpos/brickRows * j
            bricks.append(Brick(Vector2(x + brickW/2, y + brickH/2), Vector2(brickW, brickH), health=randint(1, 4)))

# Balls configuration
ballSpeed = 3
speedMult = 1
ballRadius = 10
ballColor = RED
initialBallPos = Vector2(WIDTH/2, HEIGHT - movePadGroundDistance - 50)
initialBallVel = Vector2(randint(-100, 100)/100, -1)
balls: list[Ball] = []
balls.append(Ball(initialBallPos, initialBallVel, ballSpeed, ballRadius, ballColor))

# Powerups
maxBalls = 500
speedOnSlow = .125
speedOnFast = 5
padSizeOnBig = 140
padSizeOnSmall = 45
doubleBallsKey = K_e
slowBallsKey = K_x
fastBallsKey = K_z
bigPadKey = K_f
smallPadKey = K_g

while True:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    mousePos = Vector2(mouseX, mouseY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == doubleBallsKey:
                if len(balls) == 0:
                    balls.append(Ball(initialBallPos, initialBallVel, ballSpeed, ballRadius, ballColor))
                else:
                    for ball in balls[:]:
                        if len(balls) >= maxBalls:
                            break
                        balls.append(Ball(ball.pos, Vector2(ball.vel.x * (randint(-10, 10)/10) + 1, ball.vel.y * (randint(0, 25)/10) + 1), ball.speed, ball.radius, ball.color))
                print(len(balls))
            elif event.key in (K_a, K_LEFT):
                xMove -= 1
            elif event.key in (K_d, K_RIGHT):
                xMove += 1
            elif event.key == bigPadKey:
                if movePad.width == padSizeOnBig:
                    movePad.width = movePadW
                else:
                    movePad.width = padSizeOnBig
            elif event.key == smallPadKey:
                if movePad.width == padSizeOnSmall:
                    movePad.width = movePadW
                else:
                    movePad.width = padSizeOnSmall
        elif event.type == KEYUP:
            if event.key in (K_a, K_LEFT):
                xMove += 1
            elif event.key in (K_d, K_RIGHT):
                xMove -= 1

    keysPressed = pygame.key.get_pressed()
    if keysPressed[slowBallsKey] and not keysPressed[fastBallsKey]:
        speedMult = speedOnSlow
    elif keysPressed[fastBallsKey] and not keysPressed[slowBallsKey]:
        speedMult = speedOnFast
    else:
        speedMult = 1

    # Clear screen
    window.fill(WHITE)

    # Update pad position
    if movementWithKeyboard:
        movePad.pos.x = clamp(movePad.pos.x + xMove * moveSpeed, movePad.width/2, WIDTH - movePad.width/2)
    else:
        movePad.pos.x = clamp(mouseX, movePad.width/2, WIDTH - movePad.width/2)

    # Draw the player pad
    movePad.draw(drawOutline=False)

    # Update and draw bricks
    for brick in bricks[:]:
        if brick.health <= 0:
            bricks.remove(brick)
            continue

    # Update balls
    for ball in balls[:]:
        touchedGround = ball.update()
        if touchedGround:
            balls.remove(ball)

    # Draw bricks
    for brick in bricks:
        brick.draw()

    # Draw all balls
    for ball in balls:
        ball.draw()


    pygame.display.update()
    clock.tick(FPS)

''''
TODO:
 - Criar uma classe Powerup que tem as propriedades radius, fallSpeed, color (ou textureFileName) e um método activate()
        - O powerup.pos.y aumenta em fallSpeed a cada frame
        - O método activate() é chamado quando o powerup encosta (colide) com o movePad
                - Aqui que rola a putaria.
                - Da pra meter uma propriedade duration tbm, que reverte oq foi feito depois de um tempo
                        - Teria q meter um coroutine.wrap() mas n faço ideia de como fazer lmao
                        - Ou fazer um método done() q verifica a cada frame no while True e se retornar true,
                          tira da lista e chama o método stop()/revert()
 - Sistema de jogo:
        - Se não houver nenhuma bola, perdeu o jogo
        - Se não houver nenhum tijolo, ganhou o jogo
 - Mudar a cor/textura dos tijolos de acordo com a vida/maxVida deles

'''