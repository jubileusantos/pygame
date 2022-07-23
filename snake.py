import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
from random import randint
from math import floor
from time import time

pygame.init()
WIDTH = 1300
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

# Constants
CELL_SIZE = 10
SNAKE_MOVE_TIME = .1
COLS = floor(WIDTH / CELL_SIZE)
ROWS = floor(HEIGHT / CELL_SIZE)
LINE_WIDTH = 1
WORLD_OFFSET = Vector2(0, 0)
OFFSCREEN_CELLS_FRUIT_SPAWN = 15
# Colors
BACKGROUND_COLOR = (130, 130, 130)
SNAKE_COLOR = GREEN
FRUIT_COLOR = RED
LINE_COLOR = (30, 30, 30)

# States
mouseDown = False
cameraLocked = False
followButtonDown = False

# Function to add a fruit randomly on the grid
def addFruit() -> None:
    # Get offset and position constraints
    offsetX = WORLD_OFFSET.x // CELL_SIZE * CELL_SIZE
    offsetY = WORLD_OFFSET.y // CELL_SIZE * CELL_SIZE
    minX = -offsetX/CELL_SIZE - OFFSCREEN_CELLS_FRUIT_SPAWN
    maxX = -offsetX/CELL_SIZE + COLS + OFFSCREEN_CELLS_FRUIT_SPAWN
    minY = -offsetY/CELL_SIZE - OFFSCREEN_CELLS_FRUIT_SPAWN
    maxY = -offsetY/CELL_SIZE + ROWS + OFFSCREEN_CELLS_FRUIT_SPAWN

    while True:
        # Get random position
        x = randint(floor(minX), floor(maxX))
        y = randint(floor(minY), floor(maxY))

        # Check if there is no snake in the chosen cell
        valid = True
        for snake in snakes:
            for segment in snake.getBody():
                if segment.x == x and segment.y == y:
                    valid = False
                    break
            
            if not valid:
                break

        # Check for fruits as well
        for fruit in fruits:
            if fruit.pos.x == x and fruit.pos.y == y and valid:
                valid = False
                break

        # If it's valid, add a fruit
        if valid:
            print(f"Added fruit on pos ({x}, {y})")
            fruits.append(Fruit(Vector2(x, y)))
            break

# Function to draw grid
def drawGrid() -> None:
    offsetX = WORLD_OFFSET.x // CELL_SIZE * CELL_SIZE
    offsetY = WORLD_OFFSET.y // CELL_SIZE * CELL_SIZE
    for x in range(COLS):
        pygame.draw.line(window, LINE_COLOR, (x * CELL_SIZE, 0),
                                             (x * CELL_SIZE, HEIGHT), LINE_WIDTH)

    for y in range(ROWS):
        pygame.draw.line(window, LINE_COLOR, (0,     y * CELL_SIZE),
                                             (WIDTH, y * CELL_SIZE), LINE_WIDTH)

# Function to show game over screen
def gameOver() -> None:
    pass

def focusSnake() -> None:
    snakeHead = snakes[0].getBody()[0]
    WORLD_OFFSET.x = (-snakeHead.x + COLS/2) * CELL_SIZE
    WORLD_OFFSET.y = (-snakeHead.y + ROWS/2) * CELL_SIZE
    print(WORLD_OFFSET)

class Direction:
    Up = Vector2(0, -1)
    Down = Vector2(0, 1)
    Left = Vector2(-1, 0)
    Right = Vector2(1, 0)

class Fruit:
    def __init__(self, pos: Vector2, color: tuple=None) -> None:
        self.pos = pos
        self.color = color or FRUIT_COLOR
    
    def draw(self) -> None:
        offsetX = WORLD_OFFSET.x // CELL_SIZE * CELL_SIZE
        offsetY = WORLD_OFFSET.y // CELL_SIZE * CELL_SIZE
        pygame.draw.rect(window, self.color, (self.pos.x * CELL_SIZE + offsetX,
                                              self.pos.y * CELL_SIZE + offsetY, CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self, startPos: Vector2=None, startLength: int=4, color: tuple=None) -> None:
        self.color = color or SNAKE_COLOR
        self.startPos = startPos or Vector2(WIDTH/CELL_SIZE/2, HEIGHT/CELL_SIZE/2)
        self.startLength = startLength
        self.direction = Direction.Right
        self.__lastMove = time()
        self.createBody()

        # To prevent changing direction more than once before moving again, create a debounce
        self.__directionDebouce = False

    def getBody(self) -> list[Vector2]:
        return self.__body[:]

    def createBody(self) -> None:
        # Clear body
        self.__body: list[Vector2] = []

        # Reset direction
        self.direction = Direction.Right

        # Add segments
        for i in range(self.startLength):
            self.__body.append(self.startPos - self.direction * i)

    def move(self) -> None:
        if not time() > self.__lastMove + SNAKE_MOVE_TIME:
            return
        self.__lastMove = time()

        # Get current and next head position
        headPos = self.__body[0]
        nextPos = headPos + self.direction
        # Add new segment at index 0
        self.__body.insert(0, nextPos)

        # Check if snake ate a fruit
        ateFruit = False
        for fruit in fruits:
            if fruit.pos.x == nextPos.x and fruit.pos.y == nextPos.y:
                ateFruit = True
                fruits.remove(fruit)
                addFruit()
                break

        if not ateFruit:
            # Remove tail
            self.__body.pop()

        # Change direction debounce
        self.__directionDebouce = False

        # Check if is dead
        if self.isDead():
            # gameOver()

            # Restart snake
            self.createBody()

    def changeDirection(self, newDirection: Vector2) -> None:
        if newDirection != self.direction and newDirection != -self.direction and not self.__directionDebouce:
            self.__directionDebouce = True
            self.direction = newDirection

    def isDead(self) -> bool:
        head = self.__body[0]
        for segment in self.__body[1:]:
            if segment.x == head.x and segment.y == head.y:
                return True

        return False

    def draw(self) -> None:
        for segmentPos in self.__body:
            offsetX = WORLD_OFFSET.x // CELL_SIZE * CELL_SIZE
            offsetY = WORLD_OFFSET.y // CELL_SIZE * CELL_SIZE
            x = CELL_SIZE * floor(segmentPos.x) + offsetX
            y = CELL_SIZE * floor(segmentPos.y) + offsetY

            pygame.draw.rect(window, self.color, (x, y, CELL_SIZE, CELL_SIZE))

# Lists of snakes and fruits
snakes: list[Snake] = []
fruits: list[Fruit] = []

# Create a snake
snake = Snake(startLength=7)
snakes.append(snake)

# Add random fruits
for i in range(15):
    addFruit()

while True:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    mousePos = Vector2(mouseX, mouseY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key in (K_w, K_UP):
                snake.changeDirection(Direction.Up)
            elif event.key in (K_a, K_LEFT):
                snake.changeDirection(Direction.Left)
            elif event.key in (K_s, K_DOWN):
                snake.changeDirection(Direction.Down)
            elif event.key in (K_d, K_RIGHT):
                snake.changeDirection(Direction.Right)
            elif event.key == K_f:
                head = snakes[0].getBody()[0]
                offsetX = WORLD_OFFSET.x // CELL_SIZE * CELL_SIZE
                offsetY = WORLD_OFFSET.y // CELL_SIZE * CELL_SIZE
                print(f"Snake Head Pos: ({head.x:.0f}, {head.y:.0f})\nWorld Offset: ({offsetX:.0f}, {offsetY:.0f})")
            elif event.key == K_y:
                cameraLocked = not cameraLocked
            elif event.key == K_SPACE:
                followButtonDown = True
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                followButtonDown = False
        elif event.type == MOUSEMOTION and mouseDown:
            WORLD_OFFSET += Vector2(event.rel[0], event.rel[1])

    # Get mouse buttons state
    left, middle, right = pygame.mouse.get_pressed(3)
    mouseDown = left

    window.fill(BACKGROUND_COLOR)
    # print(floor(WORLD_OFFSET.x), floor(WORLD_OFFSET.y))

    for fruit in fruits:
        fruit.draw()

    # Move all snakes
    for snake in snakes:
        snake.move()

    if cameraLocked or followButtonDown:
        # Focus "camera" on snake
        focusSnake()

    # Draw snakes
    for snake in snakes:
        snake.draw()

    drawGrid()

    pygame.display.set_caption(f"Snake | FPS: {clock.get_fps():.0f}")
    pygame.display.update()
    clock.tick(FPS)

'''
DONE:
 - Desenhar as linhas corretamente de acordo com o WORLD_OFFSET
 - Quando o usuário apertar um botão (espaço, Y ou sla), focar a "câmera" na cobra

TODO:
 - Se não tiver nenhum fruta no campo de visão, colocar uma seta na tela apontando para a fruta mais próxima

'''