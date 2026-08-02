import sys
import math
import pygame

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("complex")

clock = pygame.time.Clock()
SCALE = 1/150
NUM_LINES = 200




CIRCLE_COLOR_NORMAL = (0, 150, 255)
CIRCLE_COLOR_CLICKED = (255, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = WHITE




circle_radius = 5
current_color = CIRCLE_COLOR_NORMAL

def grid(screen, resolution=10):
    x_start = 0
    y_start = 0

    x_end = WIDTH
    y_end = HEIGHT

    x_step = int(WIDTH/resolution)
    # y_step = int(HEIGHT/resolution)

    for x in range(x_start, x_end, x_step):
        pygame.draw.line(screen, BLACK, (x, y_start), (x, y_end), width=2)

    for y in range(y_start, y_end, x_step):
        pygame.draw.line(screen, BLACK, (x_start, y), (x_end, y), width=2)



def sqc(point, shift=(0,0)):
    x = point[0]
    y = point[1]

    exploded = False
    try:
        # c = complex(x - shift[0], y - shift[1]) ** 2
        c = complex(x, y) ** 2 + complex(shift[0], shift[1])

        if abs(c) > 2:
            return (
                c.real,
                c.imag,
                True,
            )
    except:
        # print(e)
        c = complex(x, y)
        exploded = True
    return (
        c.real,
        c.imag,
        exploded
    )
    
    





def n(point):
    # centers the stuff
    x = point[0]
    y = point[1]

    return (
        (x - WIDTH/2) * SCALE,
        (y - HEIGHT/2) * SCALE,
    )

def s(point):
    # centers the stuff
    x = point[0]
    y = point[1]

    return (
        x/SCALE + WIDTH/2,
        HEIGHT/2  + y/SCALE,
    )



    




running = True

def escapes(z, shift, MAX_ITER=25):

    _x, _y = z[0] , z[1]

    # print(f"pos: {_x}, {_y}")
    for count in range(MAX_ITER):
        _x1, _y1, exploded = sqc((_x , _y ), shift)

        _x, _y = _x1, _y1
        if exploded:
            # print("Exploded")
            return True, _x, _y, count

    return False, _x, _y, count






main_mouse_x, main_mouse_y = 0, 0
shift_x, shift_y = 0, 0
shift_moving = False
both_locked = False

def to_color(p):
    x = p[0]
    y = p[1]
    return (x % 255, y %255, 100)


while running:

    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                both_locked = not both_locked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                current_color = CIRCLE_COLOR_CLICKED
                shift_moving = not shift_moving
                print(f"Left clicked at position: {n(event.pos)}")

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                current_color = CIRCLE_COLOR_NORMAL

    mouse_pos = pygame.mouse.get_pos()
    if shift_moving:
        shift_x, shift_y = n(mouse_pos)
    else:
        main_mouse_x, main_mouse_y = n(mouse_pos)

    if both_locked:
        shift_x, shift_y = n(mouse_pos)
        main_mouse_x, main_mouse_y = n(mouse_pos)






    screen.fill(BACKGROUND_COLOR)
    pygame.draw.line(screen, (220, 220, 220), (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 8)
    pygame.draw.line(screen, (220, 220, 220), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 8)
    pygame.draw.circle(screen, RED, s((main_mouse_x, main_mouse_y)), 10)
    pygame.draw.circle(screen, BLACK, s((0, 0)), int(1 / SCALE), width=1)



    # the complex attractor point
    shift = (shift_x, shift_y)
    pygame.draw.circle(screen, GREEN, s(shift), 5)

    
    _x, _y = main_mouse_x , main_mouse_y
    # _x, _y = _x * SCALE, _y * SCALE


    # print(f"pos: {_x}, {_y}")
    # for x in range(NUM_LINES):
    #     _x1, _y1, exploded = sqc((_x , _y ), shift)
    #
    #     pygame.draw.line(screen, RED, s((_x, _y)), s((_x1, _y1)), width=3)
    #
    #     _x, _y = _x1, _y1
    # pygame.draw.circle(screen, current_color, (_x, _y), circle_radius)




    grid(screen)


    MAX_ITER = 10
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # julia
            # res, _x, _y, count = escapes(n((x, y)), shift=shift, MAX_ITER=MAX_ITER)

            #mandelbrot
            res, _x, _y, count = escapes((0, 0), shift=n((x, y)), MAX_ITER=MAX_ITER)



             
            if res:


                screen.set_at((x, y), (255 * (count/MAX_ITER) ** 2,  255 * count/MAX_ITER, (count/MAX_ITER)**0.5))

            else:
                # screen.set_at((x, y), (0, 255 * count/MAX_ITER,  255 * count/MAX_ITER ))
                screen.set_at((x, y), BLACK)





            # screen.set_at((x, y), to_color((_x, _y)))



    pygame.display.flip()

    clock.tick(1)
    print("frame")
    # clock.tick(240)


pygame.quit()
sys.exit()

