import pygame
import random
import numpy as np

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# game speed
fps = 60
timer = pygame.time.Clock()

# game variables
wall_thickness = 10
# TODO: fill me in
scale = 2  # 2 pixels per meter
min_vel = 0.08  # may need to adjust 

# TODO: fill me in
rho = None  # density of the fluid body
C = None  # drag coefficient, can depend on Reynolds number, roughness of surface, etc.

gravity = np.double(9.8 / fps / scale)


class Particle:
    def __init__(
        self, x_pos, y_pos, radius, color, mass, x_vel, y_vel, id, retention=0.9
    ):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.id = id
        self.retention = retention
        self.circle = None
        self.rca = None  # TODO: Fill me in with most of the drag equation using numpy

    def draw(self):
        # TODO: change the values to use the
        self.circle = pygame.draw.circle(
            screen, self.color, (int(self.x_pos), int(self.y_pos)), self.radius
        )

    def apply_gravity(self):
        # TODO:
        # 1) check if particle is above the bottom of the screen (HEIGHT)
        # 2) adjust y_vel based on gravity constant  (this happens with each frame)
        if self.y_pos < (HEIGHT - wall_thickness / 2 - self.radius - 1):
            self.y_vel += gravity

    def apply_drag(self):
        # TODO: fill me in with numpy, remember to scale for 60 fps and update velocity
        pass

    def update_position(self):
        # TODO:
        # adjust x and y pos based on velocity
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def wall_bounce(self):
        # check bottom
        if self.y_pos > (HEIGHT - wall_thickness / 2 - self.radius):
            self.y_vel *= -1 * self.retention
            self.y_pos = HEIGHT - wall_thickness / 2 - self.radius
            if self.y_vel > -0.5:  # this line may need to be adjusted sometimes
                self.y_vel = 0

        # check top
        if self.y_pos < (wall_thickness / 2 + self.radius):
            self.y_vel *= -1 * self.retention
            self.y_pos = wall_thickness / 2 + self.radius
            # no min vel check at top due to gravity

        # check right
        if self.x_pos > (WIDTH - wall_thickness / 2 - self.radius):
            self.x_vel *= -1 * self.retention
            self.x_pos = WIDTH - wall_thickness / 2 - self.radius
            if abs(self.x_vel) <= min_vel:
                self.x_vel = 0

        # check left
        if self.x_pos < (wall_thickness / 2 + self.radius):
            self.x_vel *= -1 * self.retention
            self.x_pos = wall_thickness / 2 + self.radius
            if abs(self.x_vel) <= min_vel:
                self.x_vel = 0


def draw_walls():
    left = pygame.draw.line(screen, "white", (0, 0), (0, HEIGHT), wall_thickness)
    # TODO: Fill these in
    right = pygame.draw.line(
        screen, "white", (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness
    )
    top = pygame.draw.line(screen, "white", (0, 0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(
        screen, "white", (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness
    )
    walls = [left, right, top, bottom]
    return walls


p1 = Particle(WIDTH // 2, 300, 20, "blue", 300, 0, -30, 1)
ps = []
ps.append(p1)
for i in range(10):
    ps.append(
        Particle(
            random.randint(40, WIDTH - 40),
            random.randint(40, HEIGHT - 40),
            random.randint(6, 24),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            random.randint(5, 500),
            random.randint(-30, 100),
            random.randint(-30, 100),
            i,
        )
    )

# main game loop
run = True
while run:
    # run at speed
    timer.tick(fps)

    # background color
    screen.fill("black")

    walls = draw_walls()
    for p in ps:
        # call funcs here
        p.apply_gravity()
        # p.apply_drag() # TODO: uncomment me
        p.wall_bounce()
        p.update_position()
        p.draw()

    # check for events like mouse or keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exits the game loop
            run = False

    # draws everything on the screen
    pygame.display.flip()

pygame.quit()
