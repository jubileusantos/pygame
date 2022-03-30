import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
from random import randint
from math import cos, sin, radians

pygame.init()
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cock")
FPS = 60
clock = pygame.time.Clock()

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 127, 127)
PURPLE = (204, 51, 204)

class Pelo:
    def __init__(self, numSegments: int=None, color: tuple=None, thickness: int=None, segmentLen: int=160, minAngle: float=60, maxAngle: float=270) -> None:
        self.color = color or peloColor
        self.numSegments: list[Vector2] = numSegments or pelosSegments
        self.thickness = thickness or peloThickness
        #self.segmentLen = segmentLen

        # Calculate segment positions
        self.segments: list[Vector2] = []
        '''angle = randint(minAngle, maxAngle)
        r = randint(round(bolaR - bolaR/pelosRdiv), bolaR)
        x = bolaEpos.x + cos(radians(angle)) * r
        y = bolaEpos.y + sin(radians(angle)) * r
        lastPos: Vector2 = Vector2(x, y)
        self.segments.append(lastPos)
        for _ in range(self.numSegments):
            pass
            newPos = Vector2(lastPos.x + randint(-segmentLen, segmentLen), lastPos.y + randint(-segmentLen, segmentLen))
            self.segments.append(newPos)
            lastPos = Vector2(newPos.x, newPos.y)'''
        lastPos: Vector2 = None
        for i in range(self.numSegments):
            angle = randint(minAngle, maxAngle)
            r = randint(round(bolaR - bolaR/pelosRdiv), bolaR)
            x = bolaEpos.x + cos(radians(angle)) * segmentLen
            y = bolaEpos.y + sin(radians(angle)) * segmentLen
            if i == 0:
                self.segments.append(Vector2(x, y))
            x1, y1 = (lastPos and lastPos.x or x) + randint(round(-segmentLen/self.numSegments), round(segmentLen/self.numSegments)), (lastPos and lastPos.y or y) + randint(round(-segmentLen/self.numSegments), round(segmentLen/self.numSegments))
            lastPos = Vector2(x1, y1)
            self.segments.append(lastPos)

    def draw(self, surface=window) -> None:
        for i in range(len(self.segments)-1):
            seg1 = self.segments[i]
            seg2 = self.segments[i+1]
            pygame.draw.line(surface, self.color, (seg1.x + offset.x, seg1.y + offset.y), (seg1.x + offset.x, seg2.y + offset.y), self.thickness)


class Veia:
    def __init__(self) -> None:
        pass

# Estados
offset = Vector2(0, 0)
mouseDown = False
frame = 0

# Posição das partes
# Bolas
bolaEpos = Vector2(WIDTH-WIDTH//1.7, HEIGHT-150)
bolaDpos = Vector2(WIDTH//1.7, HEIGHT-150)
bolaR = 70
# Tronco
troncoW = 100
troncoH = HEIGHT-190
troncoPos = Vector2(WIDTH//2 - 50, 50)#, troncoW, troncoH)

# Pelos
peloLen = 170
numPelos = 350
pelosSegments = 15
peloThickness = 1
peloColor = (45, 25, 0)
pelosRdiv = 3.5
pelos: list[Pelo] = []
for _ in range(numPelos):
    # Angulo aleatorio entre 0 e ~210 para a bola esquerda e 180 e ~-30 para a direita
    '''pelos.append(Pelo())'''
    '''pelos.append(Pelo(minAngle=-90, maxAngle=120))'''

    pelo = []
    newX, newY = None, None
    for i in range(pelosSegments):
        angle = randint(45, 270)
        r = randint(round(bolaR - bolaR/pelosRdiv), bolaR)
        x = bolaEpos.x + cos(radians(angle)) * r
        y = bolaEpos.y + sin(radians(angle)) * r
        if i == 0:
            pelo.append((x, y))
        x1, y1 = (newX or x) + randint(round(-peloLen/pelosSegments), round(peloLen/pelosSegments)), (newY or y) + randint(round(-peloLen/pelosSegments), round(peloLen/pelosSegments))
        newX, newY = x1, y1
        pelo.append((x1, y1))
    pelos.append(pelo)

    pelo = []
    newX, newY = None, None
    for i in range(pelosSegments):
        angle = randint(-90, 135)
        r = randint(round(bolaR - bolaR/pelosRdiv), bolaR)
        x = bolaDpos[0] + cos(radians(angle)) * r
        y = bolaDpos[1] + sin(radians(angle)) * r
        if i == 0:
            pelo.append((x, y))
        x1, y1 = (newX or x) + randint(round(-peloLen/pelosSegments), round(peloLen/pelosSegments)), (newY or y) + randint(round(-peloLen/pelosSegments), round(peloLen/pelosSegments))
        newX, newY = x1, y1
        pelo.append((x1, y1))
    pelos.append(pelo)

# Veias
veiaR = 105
veiasN = 25
veiasSegmentos = 45
veiaCor = (255, 30, 0)
veiaGrossura = 3
veiaYdiv = 2
veias = []
for _ in range(veiasN):
    # Angulo aleatorio entre -37 e 37 para o lado direito e entre 143 e 217 para o lado esquerdo
    veia = []
    newX, newY = None, None
    initialAngle = randint(-37, 37)
    toLeft = True
    if randint(1, 2) == 1:
        initialAngle = randint(143, 217)
        toLeft = False
    for i in range(veiasSegmentos):
        if initialAngle is not None:
            angle = initialAngle
        else:
            angle = randint(-37, 37)
            if randint(1, 2) == 1:
                angle = randint(143, 217)
        r = randint(round(veiaR - veiaR/50), veiaR)
        x = troncoPos[0] + troncoW/2 + cos(radians(angle)) * troncoW/2
        y = troncoPos[1] + troncoH/2 + sin(radians(angle)) * troncoH/2
        if i == 0:
            veia.append((x, y))
        if toLeft:
            #x1, y1 = (newX or x) + randint(round(-veiaR/veiasSegmentos), round(veiaR/veiasSegmentos)), (newY or y) + randint(round(-veiaR/veiasSegmentos), round(veiaR/veiasSegmentos))
            x1, y1 = (newX or x) + randint(round(-veiaR/veiasSegmentos), 0), (newY or y) + randint(round(-veiaR/(veiasSegmentos/veiaYdiv)), round(veiaR/(veiasSegmentos/veiaYdiv)))
        else:
            x1, y1 = (newX or x) + randint(0, round(veiaR/veiasSegmentos)), (newY or y) + randint(round(-veiaR/(veiasSegmentos/veiaYdiv)), round(veiaR/(veiasSegmentos/veiaYdiv)))
        newX, newY = x1, y1
        veia.append((x1, y1))
        initialAngle = None
    veias.append(veia)

window.fill(WHITE)
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and mouseDown:
            offset.x += event.rel[0]
            offset.y += event.rel[1]

    leftButton, _, _ = pygame.mouse.get_pressed()
    mouseDown = leftButton

    window.fill(WHITE)

    # Bolas
    pygame.draw.circle(window, PINK, (bolaEpos.x + offset.x, bolaEpos.y + offset.y), bolaR)
    pygame.draw.circle(window, PINK, (bolaDpos.x + offset.x, bolaDpos.y + offset.y), bolaR)
    
    pygame.draw.ellipse(window, PINK, (troncoPos.x + offset.x, troncoPos.y + offset.y, troncoW, troncoH), 0)
    
    # Veias
    for veia in veias:
        for i in range(veiasSegmentos-1):
            veia1 = veia[i]
            veia2 = veia[i+1]
            pygame.draw.line(window, veiaCor, (veia1[0] + offset.x, veia1[1] + offset.y), (veia2[0] + offset.x, veia2[1] + offset.y), veiaGrossura)

    # Pelos
    '''for pelo in pelos:
        pelo.draw()'''
    for pelo in pelos:
        for i in range(pelosSegments-1):
            pelo1 = pelo[i]
            pelo2 = pelo[i+1]
            pygame.draw.line(window, peloColor, (pelo1[0] + offset.x, pelo1[1] + offset.y), (pelo2[0] + offset.x, pelo2[1] + offset.y), peloThickness)

    # Glande
    w = 85
    h = 100
    pygame.draw.ellipse(window, PURPLE, (WIDTH//2 - w/2 + offset.x, 50 + offset.y, w, h))

    # Saída glandiana
    pygame.draw.line(window, BLACK, (WIDTH//2 + offset.x, 50 + offset.y), (WIDTH//2 + offset.x, 50 + h/3 + offset.y))

    pygame.display.update()
    frame += 1
    clock.tick(FPS)