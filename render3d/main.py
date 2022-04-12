import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2, Vector3
from matrix import Matrix
import faceVertices
from random import randint
from math import cos, pi, sin, radians, inf

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

def map(n, start1, stop1, start2, stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2

def clamp(n, minVal, maxVal):
    if n < minVal:
        return minVal
    elif n > maxVal:
        return maxVal
    return n

def pointInPolygon(point: Vector2, vertices: list[Vector2]) -> bool:
    c = 0
    p1 = vertices[0]
    n = len(vertices)

    for i in range(1, len(vertices)):
        p2 = vertices[i % n]
        if (point.x > min(p1.x, p2.x) and
            point.x <= max(p1.x, p2.x) and
            point.y <= max(p1.y, p2.y) and
            p1.x != p2.x):
                xinters = (point.x - p1.x) * (p2.y - p1.y) / (p2.x - p1.x) + p1.y
                if (p1.y == p2.y or point.y <= xinters):
                    c += 1
        p1 = p2
    # if the number of edges we passed through is even, then it's not in the poly.
    return c % 2 != 0

def drawText(text: str, pos: Vector2, fontSize: int=18, fontType: str="comicsans", bold: bool=False,
             italic: bool=False, antiAlias: bool=False, textColor: tuple=BLACK, bgColor: tuple=None,
             centerX: float=0, centerY: float=0, surface: pygame.Surface=window):
    font = pygame.font.SysFont(fontType, fontSize, bold, italic)
    textSurface = font.render(str(text), antiAlias, textColor, bgColor)
    textRect = textSurface.get_rect()
    surface.blit(textSurface, [pos.x + (textRect.width/2) * centerX, pos.y + (textRect.height/2) * centerY])

class BaseObject:
    def __init__(self, pos: Vector3, color: tuple=BLACK, edgeThickness: int=1,
                 cornerThickness: int=1, faceColors: dict[str, list[int]]=None) -> None:
        self.pos = pos
        self.color = color
        self.edgeThickness = edgeThickness
        self.cornerThickness = cornerThickness
        self.rotation = Vector3(0, 0, 0)
        self.faceColors = faceColors
        self.size = 1
        self.points: list[Vector3] = []

    def rotateX(self, angle) -> None:
        self.rotation.x += radians(angle)

    def rotateY(self, angle) -> None:
        self.rotation.y += radians(angle)

    def rotateZ(self, angle) -> None:
        self.rotation.z += radians(angle)

    def getPoints(self) -> list[Vector2]:
        # Create rotation matrices
        rotationX: Matrix = Matrix([
            [1, 0, 0],
            [0, cos(self.rotation.x + radians(GLOBAL_ROTATION.x)), -sin(self.rotation.x + radians(GLOBAL_ROTATION.x))],
            [0, sin(self.rotation.x + radians(GLOBAL_ROTATION.x)),  cos(self.rotation.x + radians(GLOBAL_ROTATION.x))],
        ])
        rotationY: Matrix = Matrix([
            [cos(self.rotation.y + radians(GLOBAL_ROTATION.y)), 0, -sin(self.rotation.y + radians(GLOBAL_ROTATION.y))],
            [0, 1, 0],
            [sin(self.rotation.y + radians(GLOBAL_ROTATION.y)), 0, cos(self.rotation.y + radians(GLOBAL_ROTATION.y))],
        ])
        rotationZ: Matrix = Matrix([
            [cos(self.rotation.z + radians(GLOBAL_ROTATION.z)), -sin(self.rotation.z + radians(GLOBAL_ROTATION.z)), 0],
            [sin(self.rotation.z + radians(GLOBAL_ROTATION.z)),  cos(self.rotation.z + radians(GLOBAL_ROTATION.z)), 0],
            [0, 0, 1]
        ])

        # Save the projected points
        projectedPoints: list[Vector2] = []

        # Calculate all vertex positions
        for point in self.points:
            # Rotate
            rotated = rotationX * Matrix.fromVector3(point)
            rotated = rotationY * rotated
            rotated = rotationZ * rotated

            # Calculate projected
            if orthographicProjection:
                z = 1
            else:
                z = 1 / (GLOBAL_POSITION.z - Matrix.toVector3(rotated).z)

            projection: Matrix = Matrix([
                [z, 0, 0],
                [0, z, 0],
                [0, 0, z]
            ])
            # Add offset and scale
            projected = Matrix.toVector2(projection * rotated)
            pos = Vector2(self.pos.x + GLOBAL_POSITION.x + projected.x * self.size, self.pos.y + GLOBAL_POSITION.y + projected.y * self.size)
            projectedPoints.append(pos)
        
        return projectedPoints

    def draw(self, surface: pygame.Surface=window, drawEdges: bool=True, paintFaces: bool=False) -> None:
        pass

class Square(BaseObject):
    def __init__(self, pos: Vector3=None, size: float=50, color: tuple=BLACK, edgeThickness: int=1,
                 cornerThickness: int=1, faceColors: dict[str, list[int]]=None) -> None:
        super().__init__(pos, color, edgeThickness, cornerThickness, faceColors)
        self.size = size
        self.points: list[Vector3] = [
            # Back
            Vector3(-1, -1, -1),
            Vector3(.1, -1, -1),
            Vector3(1, 1, -1),
            Vector3(-1, 1, -1),

            # Front
            Vector3(-1, -1, 1),
            Vector3(1, -1, 1),
            Vector3(1, 1, 1),
            Vector3(-1, 1, 1),
        ]

    def draw(self, surface: pygame.Surface=window, drawEdges: bool=True, paintFaces: bool=False) -> None:
        # Get points
        projectedPoints: list[Vector2] = self.getPoints()

        # Paint faces
        if paintFaces:
            for face, indexes in faceVertices.square.items():
                if len(indexes) == 0: continue
                color = self.faceColors.setdefault(face, BLACK)

                faceList: list[Vector2] = []
                for index in indexes:
                    faceList.append(projectedPoints[index])

                pygame.draw.polygon(surface, color, faceList)

        if drawEdges:
            # Draw edges
            for i in range(0):
                pygame.draw.line(surface, self.color, projectedPoints[i], projectedPoints[(i + 1) % 4], self.edgeThickness)
                pygame.draw.line(surface, self.color, projectedPoints[i+4], projectedPoints[(i + 1) % 4 + 4], self.edgeThickness)
                pygame.draw.line(surface, self.color, projectedPoints[i], projectedPoints[i + 4], self.edgeThickness)

class Sphere(BaseObject):
    def __init__(self, pos: Vector3=None, radius: float=50, resolution: int=15, color: tuple=BLACK, edgeThickness: int=1,
                 cornerThickness: int=1, faceColors: dict[str, list[int]]=None) -> None:
        super().__init__(pos, color, edgeThickness, cornerThickness, faceColors)
        self.size = radius
        self.radius = radius
        self.resolution = resolution

        # Calculate points
        for i in range(resolution):
            lat = map(i, 0, resolution-1, 0, 2*pi)
            for j in range(resolution):
                lon = map(j, 0, resolution-1, 0, pi)

                x = self.pos.x + sin(lon) * cos(lat)
                y = self.pos.y + sin(lon) * sin(lat)
                z = self.pos.z + cos(lon)
                self.points.append(Vector3(x, y, z))

    def draw(self, surface: pygame.Surface=window, drawEdges: bool=True, paintFaces: bool=False) -> None:
        # Get points
        projectedPoints = self.getPoints()

        if paintFaces:
            # Paint faces
            for i in range(self.resolution):
                horizontalPoints: list[Vector2] = []
                for j in range(self.resolution):
                    horizontalPoints.append(projectedPoints[i + (j) * self.resolution])
                    
                # Horizontal Lines
                pygame.draw.polygon(surface, self.color, horizontalPoints)

                # Vertical Lines
                startIdx = i * self.resolution
                endIdx = i * self.resolution + self.resolution
                pygame.draw.polygon(surface, self.color, projectedPoints[startIdx:endIdx])

        if drawEdges:
            for i in range(self.resolution-1):
                for j in range(self.resolution-1):
                    idx = i + j * self.resolution
                    idx1 = i + (j+1) * self.resolution
                    # Horizontal
                    pygame.draw.line(surface, BLACK, projectedPoints[idx], projectedPoints[idx1], self.edgeThickness)
                    # Vertical
                    pygame.draw.line(surface, BLACK, projectedPoints[idx], projectedPoints[idx+1], self.edgeThickness)

# Modes
orthographicProjection = True         # If false, Perspective Projection will be used
autoResetGlobalPosition = False
autoResetGlobalRotation = False

# Movement
GLOBAL_POSITION = Vector3(0, 0, 5)
GLOBAL_ROTATION = Vector3(0, 0, 0)
positionResetLerp = .002
rotationResetLerp = .002
positionAdd = Vector3(0, 0, 0)
rotationAdd = Vector3(0, 0, 0)
positionAddCapLerp = .003
rotationAddCapLerp = .001
zoomStep = .1

# Objects
objects: list[BaseObject] = []
for i in range(1):
    faceColors = {
        "right": GREEN,
        "front": YELLOW,
        "back": BLUE,
        "top": BLACK,
        "bottom": ORANGE,
        "left": RED,
    }
    #objects.append(Square(pos=Vector3(randint(100, WIDTH-100), randint(100, HEIGHT-100), randint(1, 5)), size=150, edgeThickness=2, faceColors=faceColors))
    objects.append(Sphere(color=RED, pos=Vector3(randint(10, 30)/10, randint(10, 30)/10, 1), radius=150, resolution=25, edgeThickness=1, faceColors=faceColors))

# States
leftButtonDown = False
rightButtonDown = False

dt = 1000/FPS
while True:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    mousePos = Vector2(mouseX, mouseY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouseDown = True
        elif event.type == MOUSEBUTTONUP:
            mouseDown = False
        elif event.type == MOUSEWHEEL:
            GLOBAL_POSITION.z = clamp(GLOBAL_POSITION.z - event.y * zoomStep, 1, 1e10)
        elif event.type == MOUSEMOTION:
            if leftButtonDown:
                # If left button is pressed, move position
                positionAdd = Vector3(event.rel[0], event.rel[1], 0)
                GLOBAL_POSITION += Vector3(event.rel[0], event.rel[1], 0)
            if rightButtonDown:
                # If right button is pressed, rotate world
                rotationAdd = Vector3(-event.rel[1], -event.rel[0], 0)
                GLOBAL_ROTATION += Vector3(-event.rel[1], -event.rel[0], 0)

    # Mouse input
    left, middle, right = pygame.mouse.get_pressed()
    leftButtonDown, rightButtonDown = left, right

    window.fill(WHITE)

    # Lerp global position and rotation offsets towards zero
    # Position
    if positionAdd.length_squared() < .01:
        positionAdd = Vector3(0, 0, 0)
    else:
        positionAdd = positionAdd.lerp(Vector3(0, 0, 0), positionAddCapLerp)
    # Rotation
    if rotationAdd.length_squared() < .01:
        rotationAdd = Vector3(0, 0, 0)
    else:
        rotationAdd = rotationAdd.lerp(Vector3(0, 0, 0), rotationAddCapLerp)

    # Add global position and rotation
    if not autoResetGlobalPosition and not leftButtonDown and not rightButtonDown and positionAdd.length_squared() > 0:
        print("Adding global position")
        GLOBAL_POSITION += positionAdd * .1
    if not autoResetGlobalRotation and not rightButtonDown and not leftButtonDown and rotationAdd.length_squared() > 0:
        print("Adding global rotation")
        GLOBAL_ROTATION += rotationAdd * .1

    # Reset global position and rotation
    if not leftButtonDown and autoResetGlobalPosition and GLOBAL_POSITION != Vector3(0, 0, 0):
        if GLOBAL_POSITION.length_squared() < 1:
            GLOBAL_POSITION = Vector3(0, 0, GLOBAL_POSITION.z)
        else:
            GLOBAL_POSITION = GLOBAL_POSITION.lerp(Vector3(0, 0, GLOBAL_POSITION.z), positionResetLerp)

    if not rightButtonDown and autoResetGlobalRotation and GLOBAL_ROTATION != Vector3(0, 0, 0):
        if GLOBAL_ROTATION.length_squared() < .5:
            GLOBAL_ROTATION = Vector3(0, 0, 0)
        else:
            GLOBAL_ROTATION = GLOBAL_ROTATION.lerp(Vector3(0, 0, 0), rotationResetLerp)

    # Draw objects
    for obj in objects:
        obj.draw(paintFaces=True, drawEdges=True)

    # Show FPS
    drawText(f"FPS: {1000/dt:.0f}", Vector2(), fontSize=15)

    pygame.display.update()
    dt = clock.tick(FPS)

'''
TODO:
 - A esfera rotaciona ao redor de um outro ponto, e não em volta de si mesmo. nao faço ideia do q fazer todavia

'''