import sys
import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PI = math.pi
BG_COLOR = (30, 30, 30)
RED = (255, 30, 30)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")
clock = pygame.time.Clock()



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def val(self):
        return (self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise Exception("invalid type, must be a Point to allow addition")


    def translate(self, p: Point):
        return self + p

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def rotate(self, radians):
        _x = self.x*math.cos(radians) - self.y*math.sin(radians)
        _y = self.x*math.sin(radians) + self.y*math.cos(radians)

        return Point(
            _x,
            _y
        )

    def scale(self, scale):
        return Point(
            self.x * scale,
            self.y * scale
        )


class Hexagon:
    def __init__(self, pos: Point, size):
        self.pos = pos
        self.size = size

        # offsets
        base_point = Point(size, 0)
        one = base_point.rotate(2*PI/6)
        two = one.rotate(2*PI/6)
        three = two.rotate(2*PI/6)
        four = three.rotate(2*PI/6)
        five = four.rotate(2*PI/6)
        six = five.rotate(2*PI/6)

        self.offsets = [
            one,
            two,
            three,
            four,
            five,
            six
        ]

        # for s in self.offsets:
        #     print(s)


        self.offsets = [p.translate(self.pos) for p in self.offsets]


    

    def draw(self, screen):
        # pygame.draw.line(screen, RED, self.pos.val, (self.pos+Point(50, 50)).val, 3)
        # return

        for i in range(1, len(self.offsets)):
            a = self.offsets[i-1]
            b = self.offsets[i]

            pygame.draw.line(screen, RED, a.val, b.val, 3)


        ...
        # yes



running = True


def n(p: Point):
    return p + Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


hex1 = Hexagon(n(Point(0,0)), 25)

while running:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

 
 

 

    screen.fill(BG_COLOR)
    # pygame.draw.line(screen, RED, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2), (5, 5), 4)
    hex1.draw(screen)


 
 

    pygame.display.flip() 
    clock.tick(FPS)      

pygame.quit()
sys.exit()
