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
rho = 1.22  # density of the fluid body
C = .47  # drag coefficient, can depend on Reynolds number, roughness of surface, etc.

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
        self.rca = np.multiply(.5 * rho * C * np.pi, np.square(self.radius))  # TODO: Fill me in with most of the drag equation using numpy

    def draw(self):
        # TODO: change the values to use the
        self.circle = pygame.draw.circle(
            screen, self.color, (int(self.x_pos), int(self.y_pos)), self.radius
        )

    def apply_gravity(self):
        # TODO:
        # 1) check if particle is above the bottom of the screen (HEIGHT)
        # 2) adjust y_vel based on gravity constant  (this happens with each frame)
        # TODO: what if terminal vel is less than change in vel in a frame?
        if self.y_pos < (HEIGHT - wall_thickness / 2 - self.radius - 1):
            self.y_vel = np.add(gravity, self.y_vel)

    def apply_drag(self):
        # TODO: fill me in with numpy, remember to scale for 60 fps and update velocity
        vels = np.array([self.x_vel, self.y_vel])
        
        a = np.multiply(np.multiply(self.rca, np.square(vels)), 1/self.mass)
        # scale a for fps and pix-meter scale
        a = np.multiply(a, 1/fps * 1/scale)
        # make a in the opposite direction of motion 
        a = np.multiply(-1*np.sign(vels), a)
         
        # update the velocities with a
        out = np.add(vels, a)
        
        # TODO: fill in clipping and discrete time correction
        # PROBLEM OF DISCRETE vs. CONTINUOUS TIME
        # in reality, the acceleration from drag should never exceed the current velocity. However, we are applying it over discrete time steps rather than infintesimally small changes in time (where we could have small updates). 
        # if the acceleration from the force of drag exceeds the velocity of the direction of motion in a single frame update, then we stop (remember drag works opposite the direction of motion but if motion is changing very rapidly then our timestep won't capture it correctly)
        # TODO: explain about terminal velocity (ignoring boyouancy). What is v when drag force = grav force? what happens when we start with y_vel > terminal? should slowly slow down to terminal vel.
        # out[np.abs(vels) <= np.abs(a)] = 0 

        # check for min vel and clip (only needed in x direction)
        out[0] = 0 if (np.abs(out[0]) <= min_vel) else out[0]
        
        self.x_vel = out[0]
        self.y_vel = out[1]

    def update_position(self):
        # TODO:
        # adjust x and y pos based on velocity
        self.x_pos = np.add(self.x_vel, self.x_pos)
        self.y_pos = np.add(self.y_vel, self.y_pos)

    def wall_bounce(self):
        # check bottom
        if self.y_pos > (HEIGHT - wall_thickness / 2 - self.radius):
            self.y_vel = np.multiply(self.y_vel, -self.retention)
            self.y_pos = HEIGHT - wall_thickness / 2 - self.radius
            if self.y_vel > -0.5:  # this line may need to be adjusted sometimes
                self.y_vel = 0

        # check top
        if self.y_pos < (wall_thickness / 2 + self.radius):
            self.y_vel = np.multiply(self.y_vel, -self.retention)
            self.y_pos = wall_thickness / 2 + self.radius
            # no min vel check at top due to gravity

        # check right
        if self.x_pos > (WIDTH - wall_thickness / 2 - self.radius):
            self.x_vel = np.multiply(self.x_vel, -self.retention)
            self.x_pos = WIDTH - wall_thickness / 2 - self.radius
            if abs(self.x_vel) <= min_vel:
                self.x_vel = 0

        # check left
        if self.x_pos < (wall_thickness / 2 + self.radius):
            self.x_vel = np.multiply(self.x_vel, -self.retention)
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


p1 = Particle(WIDTH // 2, 50, 20, "blue", 300, 0, 5, 0)
ps = []
ps.append(p1)
for i in range(1, 10):
    ps.append(
        Particle(
            random.randint(40, WIDTH - 40),
            random.randint(40, HEIGHT - 40),
            random.randint(6, 24),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            random.randint(5, 500),
            random.randint(-100, 100),
            random.randint(-100, 100),
            i,
        )
    )

# main game loop
run = True
show_info = True
time_check = 0
while run:
    # run at speed
    timer.tick(fps)

    # background color
    screen.fill("black")

    walls = draw_walls()
    for p in ps:
        # call funcs here
        p.apply_drag() # note, apply drag prior to gravity to reach terminal velocity correctly
        p.apply_gravity()        
        p.wall_bounce()
        p.update_position()
        p.draw()
        # TODO: show that the blue ball reaches terminal velocity (minus the drag)
        if p.id==0 and (pygame.time.get_ticks()//500 > time_check) and show_info:
            time_check += 1
            print(p.y_vel)

    # check for events like mouse or keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exits the game loop
            run = False

    # draws everything on the screen
    pygame.display.flip()

pygame.quit()
