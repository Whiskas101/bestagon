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
BLUE = (30, 40, 255)



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")
clock = pygame.time.Clock()



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __hash__(self): 
        # this is critical to avoid floating point errors
        # other wise it will create hexagons infinitely close, but not quite
        # at the same positions. Ruining a lifetime debugging.
        return hash(
            self.ival
        )

    def __eq__(self, other):
        if isinstance(other, Point):
            x, y = self.ival
            _x, _y = other.ival
            return _x == x and _y == y
        raise Exception(f"{other} is not a Point type")

    @property
    def val(self):
        return (self.x, self.y)

    @property
    def ival(self):
        # for adding or removing items within the map 
        # without accumulating floating point math error
        return (round(self.x), round(self.y))

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise Exception("invalid type, must be a Point to allow addition")


    def translate(self, p: Point):
        if not isinstance(p, Point):
            raise Exception("p must be a Point")


        return self + p

    def __repr__(self):
        # return f"Point({self.x}, {self.y})"
        return f"Point({self.ival})"


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
    def __init__(self, pos: Point, size, omit=(),color=RED):
        self.pos = pos
        self.size = size
        self.omit = omit
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
    

    def draw(self, screen, transform_func=None):
        # pygame.draw.line(screen, RED, self.pos.val, (self.pos+Point(50, 50)).val, 3)
        # return
        if transform_func is None:
            transform_func = lambda x : x

        screen_points = [
            transform_func(
                p.translate(
                    self.pos
                )
            )
            for p in self.offsets
        ]


        pygame.draw.circle(screen, BLUE, screen_points[0].val, radius=8, width=2)
        pygame.draw.circle(screen, BLUE, screen_points[1].val, radius=12, width=2)
        for i in range(1, len(screen_points)):
            if (((i-1)-3) % 6)+1 in self.omit:
                continue
            a = screen_points[i-1]
            b = screen_points[i]

            pygame.draw.line(screen, self.color, a.val, b.val, 3)

        # the last line
        if (((6-1)-3)%6)+1 in self.omit:
            return
        pygame.draw.line(
            screen,
            self.color,
            screen_points[0].val,
            screen_points[-1].val,
            3
        )



running = True


def n(p: Point):
    if not isinstance(p, Point):
        raise Exception(f"{p} is not a Point type")

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
        self.data = {}

    def __repr__(self):
        res = "Graph:\n"
        for idx, point in enumerate(self.data.items()):
            res += f"-{idx+1}-\t" + point.__repr__() + "\n"

        return res





    @staticmethod
    def mirror(n):
        # to get the mirror of the currentpoint
        # so I can mark both the bestagons as bidrectionally
        # linked
        # 1, 4   0, 3
        # 2, 5   1, 4
        # 3, 6 ->2, 5  (simple +3 modulus 6)
        # 4, 1   3, 0
        # 5, 2   4, 1
        # 6, 3   5, 2

        return (((n-1)+3) % 6) + 1 # +1 to bring back to 1-6 range

    def get_neighbour_offset(self, n) -> Point:
        base_hex = Hexagon(Point(0,0), size=25)
        hypotenuse_length = math.sqrt(3)# approximation
        rotation = 2 * PI / 12

        base_hex.scale(hypotenuse_length)
        base_hex.rotate(rotation)

        # rotated_pos = base_hex.pos.translate(node)
        # counteracting the rotation, so 1 refers to the encoding
        # specified above
        rotated_pos_offset = base_hex.offsets[((n-1) - 3) % 6]
        # rotated_pos = base_hex.offsets[1]
        # rotated_pos = base_hex.offsets[2]
        # rotated_pos = base_hex.offsets[3]
        # rotated_pos = base_hex.offsets[4]
        # rotated_pos = base_hex.offsets[5]

        return rotated_pos_offset

    def get_neighbour(self, node: Point, n, add=False) -> Point:
        neighbour_offset = self.get_neighbour_offset(n)
        neighbour_pos = neighbour_offset.translate(node)
        if not add and neighbour_pos not in self.data.keys():
            raise Exception(f"{node} does not have {n} as a neighbour")
        return neighbour_pos

    def get_neighbour_connections(self, node):

        return self.data.get(node)






    def add_neighbour(self, node: Point, n):
        if n < 1 or n > 6:
            raise Exception("Invalid neighbour")

        # add just signifies the intent: "gimme the damn point im gonna add itto the damn graph"
        neighbour_pos = self.get_neighbour(node, n, add=True) 

        # add it to the current node's neighbour list
        if self.data.get(node):
            self.data[node].add(n)
        else:
            self.data[node] = set([n])

        if self.data.get(neighbour_pos):
            self.data[neighbour_pos].add(self.mirror(n))
        else:
            self.data[neighbour_pos] = set([self.mirror(n)])








graph = Graph()
start = Point(0,0)

graph.add_neighbour(start, 1)
graph.add_neighbour(start, 2)
# graph.add_neighbour(start, 3)

two = graph.get_neighbour(start, 2)
print("Two", two)
graph.add_neighbour(two, 2)

graph.add_neighbour(two, 5)
graph.add_neighbour(two, 6)

three = graph.get_neighbour(two, 2)
graph.add_neighbour(three, 2)

four = graph.get_neighbour(three, 2)
graph.add_neighbour(four, 2)

five = graph.get_neighbour(four, 2)
graph.add_neighbour(five, 2)

six = graph.get_neighbour(four, 2)
graph.add_neighbour(six, 6)

seven = graph.get_neighbour(six, 6)
graph.add_neighbour(seven, 6)

eight = graph.get_neighbour(seven, 6)
graph.add_neighbour(seven, 5)



# THIS ONE IS BROKEN, probably a floating point math issue
# graph.add_neighbour(three, 5)






# graph.add_neighbour(start, 3)
# graph.add_neighbour(start, 4)
# graph.add_neighbour(start, 5)
# graph.add_neighbour(start, 6)

# second = graph.data.get(start)
# graph.

print(graph)








# make it so that the hexagon does NOT draw the parts where
# it is connected.



hexes = []
for point in graph.data:
    if not isinstance(point, Point):
        raise Exception("what are you doing")
    
    hexes.append(
        Hexagon(
            point, 
            size=25, 
            omit=graph.get_neighbour_connections(point),
            # color = (int(point.x) % 256, int(point.y) % 256, 250)
        )
    )














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
        
    # hex_b.draw(screen)
    for hex in hexes:
        hex.draw(screen, n)


    # for h in _hex_grid:
    #     h.draw(screen)






    pygame.display.flip() 
    clock.tick(FPS)      

pygame.quit()
sys.exit()
