import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2, Vector3
from random import randint
from math import cos, pi, sin, radians, inf
from time import time
import rendering3d

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

class RubiksCube:
    def __init__(self, pos: Vector3, cubieSize: float, dimensions: int=3) -> None:
        self.pos = pos
        self.cubieSize = cubieSize
        self.dimensions = dimensions
        self.rotation = Vector3(0, 0, 0)
        self.cubes: list[list[list[rendering3d.Cube]]] = []

        self.faceColors = {
            "right": RED,
            "front": GREEN,
            "back": BLUE,
            "top": WHITE,
            "bottom": YELLOW,
            "left": ORANGE,
        }
        for x in range(self.dimensions):
            xList: list[list[rendering3d.Cube]] = []
            for y in range(self.dimensions):
                yList: list[rendering3d.Cube] = []
                for z in range(self.dimensions):
                    cubePos = Vector3(self.pos.x - self.cubieSize/2 + x * self.cubieSize/2, self.pos.y - self.cubieSize/2 +  y * self.cubieSize/2, self.pos.z +  z * self.cubieSize/2)
                    cube = rendering3d.Cube(cubePos, self.cubieSize, faceColors=self.faceColors)
                    yList.append(cube)
                    #self.cubes.append(cube)
                xList.append(yList)
            self.cubes.append(xList)

    ''' function rotateX(angle) {
            var cos = Math.cos(angle),
                sin = Math.sin(angle);

            for(var i = 0; i < points.length; i++) {
                var p = points[i],
                    y = p.y * cos - p.z * sin,
                    z = p.z * cos + p.y * sin;
                p.y = y;
                p.z = z;
            }
            needsUpdate = true;
        }

        function rotateY(angle) {
            var cos = Math.cos(angle),
                sin = Math.sin(angle);

            for(var i = 0; i < points.length; i++) {
                var p = points[i],
                    x = p.x * cos - p.z * sin,
                    z = p.z * cos + p.x * sin;
                p.x = x;
                p.z = z;
            }
            needsUpdate = true;
        }

        function rotateZ(angle) {
            var cos = Math.cos(angle),
                sin = Math.sin(angle);

            for(var i = 0; i < points.length; i++) {
                var p = points[i],
                    x = p.x * cos - p.y * sin,
                    y = p.y * cos + p.x * sin;
                p.x = x;
                p.y = y;
            }
            needsUpdate = true;
        }'''

    def rotateX(self, angle: float) -> None:
        self.rotation.x += angle
        # Update all cubes
        cosA = cos(radians(angle))
        sinA = sin(radians(angle))
        for cube in self.getCubes():
            cube.rotateX(angle)
            cube.pos.y = self.pos.y*0 + cube.pos.y * cosA - cube.pos.z * sinA
            cube.pos.z = self.pos.z*0 + cube.pos.z * cosA + cube.pos.y * sinA

    def rotateY(self, angle: float) -> None:
        self.rotation.x += angle
        # Update all cubes
        cosA = cos(radians(angle))
        sinA = sin(radians(angle))
        for cube in self.getCubes():
            cube.rotateY(angle)
            cube.pos.x = self.pos.x*0 + cube.pos.x * cosA - cube.pos.z * sinA
            cube.pos.z = self.pos.z*0 + cube.pos.z * cosA + cube.pos.x * sinA

    def rotateZ(self, angle: float) -> None:
        self.rotation.x += angle
        # Update all cubes
        cosA = cos(radians(angle))
        sinA = sin(radians(angle))
        for cube in self.getCubes():
            cube.rotateZ(angle)
            cube.pos.x = self.pos.x*0 + cube.pos.x * cosA - cube.pos.y * sinA
            cube.pos.y = self.pos.y*0 + cube.pos.y * cosA + cube.pos.x * sinA

    def updateCubes(self) -> None:
        totalSize = self.cubieSize * self.dimensions
        for x in range(self.dimensions):
            for y in range(self.dimensions):
                for z in range(self.dimensions):
                    self.cubes[x][y][z].pos = Vector3(self.pos.x - self.cubieSize/2 + x * self.cubieSize/2, self.pos.y - self.cubieSize/2 +  y * self.cubieSize/2, self.pos.z +  z * self.cubieSize/2)

    def getCubes(self) -> list[rendering3d.Cube]:
        cubes: list[rendering3d.Cube] = []
        for x in range(self.dimensions):
            for y in range(self.dimensions):
                for z in range(self.dimensions):
                    cubes.append(self.cubes[x][y][z])
        return cubes

    def draw(self, surface: pygame.Surface=window, drawEdges: bool=True) -> None:
        '''self.pos.x = WIDTH/2 + cos(time() * 3) * 150
        self.pos.y = HEIGHT/2 + sin(time() * 3) * 150
        self.updateCubes()'''

        '''for x in range(self.dimensions):
            for y in range(self.dimensions):
                #self.cubes[x][y][0].faceColors = {}
                self.cubes[x][y][0].pos += Vector3(0, 1, 0)
                self.cubes[x][y][1].pos += Vector3(1, 0, 0)
                self.cubes[x][y][2].pos += Vector3(-1, 0, 0)'''

        #self.rotateX(1)

        for cube in self.getCubes():
            cube.draw(surface, drawEdges=drawEdges, paintFaces=True)

rubiksCube = RubiksCube(Vector3(WIDTH/2, HEIGHT, 0), 150)

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
    
    rubiksCube.draw(surface=window, drawEdges=True)

    # Show FPS
    drawText(f"FPS: {clock.get_fps():.0f}", Vector2(), fontSize=15)

    pygame.display.update()
    clock.tick(FPS)