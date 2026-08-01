import sys
import random
import pygame
import math
import time
from functools import lru_cache

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
FPS = 60

PI = math.pi
BG_COLOR = (255, 255, 255)
RED = (255, 30, 30)
GREEN = (30, 255, 30)
BLUE = (30, 40, 255)



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")
clock = pygame.time.Clock()



class Point:
    def __init__(self, x, y, precision=6):
        self.x = round(float(x), precision)
        self.y = round(float(y), precision)


    def __hash__(self): 
        # this is critical to avoid floating point errors
        # other wise it will create hexagons infinitely close, but not quite
        # at the same positions. Ruining a lifetime debugging.
        # return hash(
        #     self.ival
        # )
        return hash(
            (self.x, self.y)
        )

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def dist(self, p: Point):
        if not isinstance(p, Point):
            raise Exception(f"{p} should be a point")
        return math.sqrt(
            (self.x - p.x)**2 + (self.y - p.y)**2
        )


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
        return f"Point({self.x}, {self.y})"
        # return f"Point({self.ival})"


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
        if not isinstance(pos, Point):
            raise Exception(f"{pos} is not a Point")
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


        # pygame.draw.circle(screen, BLUE, screen_points[0].val, radius=8, width=2)
        # pygame.draw.circle(screen, BLUE, screen_points[1].val, radius=12, width=2)
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
    def __init__(self, hex_size=25):
        self.data = {}
        self.hex_size = hex_size

    def __repr__(self):
        res = "Graph:\n"
        for idx, point in enumerate(self.data.items()):
            res += f"-{idx+1}-\t" + point.__repr__() + "\n"

        return res


    def floating_point_precision_check(self):
        # a very, very basic check to see if there's
        # two nodes that are TOO damn close to each other.
        # O(n^2) but should be fine since my graphs are tiny
        nodes = list(self.data.keys())
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):

                p1 = nodes[i]
                p2 = nodes[j]

                if p1.dist(p2) < 1.0:
                    raise Exception(
                        f"""

                        There's some duplicate node too close to another
                            {p1} \n<>\n {p2}
                        {self.data}
                        \n\n
                        { self }

                        """
                    )
        print("Graph invariant is fine")
                    
        
        








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

    @lru_cache
    def get_neighbour_offset(self, n) -> Point:
        base_hex = Hexagon(Point(0,0), size=self.hex_size)
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
        if not isinstance(node, Point):
            raise Exception(f"{node} node better be a point")
        neighbour_offset = self.get_neighbour_offset(n)
        neighbour_pos = neighbour_offset.translate(node)
        if not add and neighbour_pos not in self.data.keys():
            raise Exception(f"{node} does not have {n} as a neighbour")
        return neighbour_pos

    def get_neighbour_connections(self, node: Point):
        if not isinstance(node, Point):
            raise Exception(f"{node}: node must be a point")
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

    def get_hexagons(self):
        hexes = []
        for point in self.data:
            if not isinstance(point, Point):
                raise Exception("what are you doing")
            
            hexes.append(
                Hexagon(
                    point, 
                    size=self.hex_size, 
                    omit=self.get_neighbour_connections(point),
                    # color = (int(point.x) % 256, int(point.y) % 256, 250)
                )
            )
        return hexes







# graph = Graph()
# start = Point(0,0)
#
# graph.add_neighbour(start, 1)
# graph.add_neighbour(start, 2)
# # graph.add_neighbour(start, 3)
#
# two = graph.get_neighbour(start, 2)
# print("Two", two)
# graph.add_neighbour(two, 2)
#
# graph.add_neighbour(two, 5)
# graph.add_neighbour(two, 6)
#
# three = graph.get_neighbour(two, 2)
# graph.add_neighbour(three, 2)
#
# four = graph.get_neighbour(three, 2)
# graph.add_neighbour(four, 2)
#
# five = graph.get_neighbour(four, 2)
# graph.add_neighbour(five, 2)
#
# six = graph.get_neighbour(four, 2)
# graph.add_neighbour(six, 6)
#
# seven = graph.get_neighbour(six, 6)
# graph.add_neighbour(seven, 6)
#
# eight = graph.get_neighbour(seven, 6)
# graph.add_neighbour(seven, 5)
#
#
# graph.floating_point_precision_check()
#
# print(graph)
#

def generate_random_hexagon_maze(n: int):
    if not isinstance(n, int):
        raise Exception("dont be an idiot")


    g = Graph()

    node = Point(0,0)
    nodes = [node]
    decisions = []
    for x in range(n):
        _n = random.randint(1,6)
        g.add_neighbour(node, _n)
        decisions.append(_n)
        cur_neighbours = g.get_neighbour_connections(node)
        choice = random.choice(list(cur_neighbours))

        node = g.get_neighbour(node, choice)
        nodes.append(node)


    print("Decisions:")
    print(decisions)
    print("nodes:")
    print(nodes)

    return g


        














# make it so that the hexagon does NOT draw the parts where
# it is connected.



# hexes = []
# for point in graph.data:
#     if not isinstance(point, Point):
#         raise Exception("what are you doing")
#
#     hexes.append(
#         Hexagon(
#             point, 
#             size=25, 
#             omit=graph.get_neighbour_connections(point),
#             # color = (int(point.x) % 256, int(point.y) % 256, 250)
#         )
#     )














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









G = Graph(hex_size=15)

node = Point(0,0)
nodes = [node]
decisions = []

time = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False






    time +=1 

    # G = generate_random_hexagon_maze(time)


    bias_factor = 5
    _n = random.randint(1,6)
    for x in range(bias_factor):
        G.add_neighbour(node, _n)
        decisions.append(_n)
        cur_neighbours = G.get_neighbour_connections(node)
        choice = random.choice(list(cur_neighbours))
        node = G.get_neighbour(node, choice)
        nodes.append(node)


    G.floating_point_precision_check()
    hexes = G.get_hexagons()
    print("TIME:", time)

    
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
