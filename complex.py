import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("complex")

clock = pygame.time.Clock()
SCALE = 1/200
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



def sqc(point, shift=(1,1)):
    x = point[0]
    y = point[1]

    try:
        c = complex(x - shift[0], y - shift[1]) ** 2
    except:
        c = complex(x, y)
    return (
        c.real,
        c.imag,
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


main_mouse_x, main_mouse_y = 0, 0
shift_x, shift_y = 0, 0
shift_moving = False
both_locked = False

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


    print(f"pos: {_x}, {_y}")
    for x in range(NUM_LINES):
        _x1, _y1 = sqc((_x , _y ), shift)
        # _x1, _y1 = sqc((_x , _y ))

        pygame.draw.line(screen, RED, s((_x, _y)), s((_x1, _y1)), width=3)

        _x, _y = _x1, _y1

    # pygame.draw.circle(screen, current_color, (_x, _y), circle_radius)

    grid(screen)


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
