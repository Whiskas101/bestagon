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
GREEN = (30, 255, 30)


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
    def __init__(self, pos: Point, size, color=RED):
        self.pos = pos
        self.size = size
        self.color = color

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



    def rotate(self, radian):
        self.offsets = [s.rotate(radian) for s in self.offsets]
        
    def scale(self, scale):
        self.offsets = [s.scale(scale) for s in self.offsets]
    

    def draw(self, screen):
        # pygame.draw.line(screen, RED, self.pos.val, (self.pos+Point(50, 50)).val, 3)
        # return

        screen_points = [p.translate(self.pos) for p in self.offsets]

        for i in range(1, len(screen_points)):
            a = screen_points[i-1]
            b = screen_points[i]

            pygame.draw.line(screen, self.color, a.val, b.val, 3)
        pygame.draw.line(screen, self.color, screen_points[0].val, screen_points[-1].val, 3)
        ...
        # yes



running = True


def n(p: Point):
    return p + Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


def nested_hexagon(grid_x=5, grid_y=15):
    size = 25
    positions = []
    # origin = n(Point(0, 0))
    origin = Point(0, 0)

    for x in range(1, grid_x + 1):
        for y in range(1, grid_y + 1):
            # yesh
            base_x = origin.x
            base_y = origin.y

            _x = 3 * size * x + (size * 3/2 * (y % 2 == 0)) + base_x
            _y = math.sin(2*PI/6)  * 1* size * y + base_y
            positions.append(Point(_x, _y))

    hexes = []
    for pos in positions:
        hexes.append(
            Hexagon(pos, size)
        )

    print(f"hexes: {len(hexes)}")
    return hexes





# graph stuff
# the goal is to represent each hexagon as a node, with a maximal of 
# six neighbours
# then, to render it as needed

# using implicit encoding, counter clockwise
# 1: topright
# 2: top
# 3: topleft
# 4: bottomleft
# 5: bottom
# 6: bottomright


class Graph:
    def __init__(self):
        self.data = {
            (0,0): set([])
        }

    def add_node(point: Point):
        if self.data.get(point) != None:
            raise Exception(f"Invalid insertion, {point} already exists")
        self.data[point] = set([])
        
    def check_distance(node: Point, n):
        raise Exception("to be implemented")
        ...

    def add_neighbour(node: Point, n):
        if n < 1 or n > 6:
            raise Exception("Invalid neighbour")

        neighbour_node = self._neighbour_position()
        if not neighbour_node:
            raise Exception("Neighbour does not exist in graph, add it first")


        self.check_distance(node, n)

        if n == 1:
            # topright
            ...
        if n == 2:
            # top
            ...
        if n == 3:
            #topleft
            ...
        if n == 4:
            #bottomleft
            ...
        if n == 5:
            #bottom
            ...
        if n == 6:
            #bottomright
            ...




        

graph = {
    Point(0,0): set([1,2,3,4,5,6]),
}










# hex1 = Hexagon(n(Point(0,0)), 25, GREEN)
# hex1.rotate(2*PI/12)
#
# hex1.scale(math.sqrt(3))
# screen_points = [p.translate(hex1.pos) for p in hex1.offsets]
# hexes = []
# for x in screen_points:
#     hexes.append(
#         Hexagon(x, hex1.size, RED)
#     )

_hex_grid = nested_hexagon(5, 15)
    







time = 0
while running:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

 
 

 

    time +=1 

    screen.fill(BG_COLOR)
    # pygame.draw.line(screen, RED, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2), (5, 5), 4)
    # hex1.draw(screen)

    # for h in hexes:
    #     h.draw(screen)

    for h in _hex_grid:
        h.draw(screen)



 
 

    pygame.display.flip() 
    clock.tick(FPS)      

pygame.quit()
sys.exit()
