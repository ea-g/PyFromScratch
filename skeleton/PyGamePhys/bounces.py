import pygame


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
gravity = None 

class Particle:
    def __init__(self, x_pos, y_pos, radius, color, mass, x_vel, y_vel, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.id = id
        self.circle = None
    
    def draw(self):
        # TODO: change the values to use the 
        self.circle = pygame.draw.circle(screen, self.color, (500, 500), 5) 
        
    def apply_gravity(self):
        # TODO: 
        # 1) check if particle is above the bottom of the screen (HEIGHT)
        # 2) adjust y_vel based on gravity constant  (this happens with each frame)
        pass
    
    def update_position(self):
        # TODO: 
        # adjust x and y pos based on velocity
        pass
        

def draw_walls():
    left = pygame.draw.line(screen, "white", (0, 0), (0, HEIGHT), wall_thickness)
    # TODO: Fill these in
    right = None
    top = None
    bottom = None
    walls = [left, right, top, bottom]
    return walls

p1 = Particle(5, 5, 50, 'blue', 300, 0, 0, 1)

# main game loop
run = True
while run:
    # run at speed 
    timer.tick(fps)
    
    # background color 
    screen.fill("black")
    
    walls = draw_walls()
    p1.draw()
    
    # call funcs here
    
    # check for events like mouse or keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exits the game loop
            run = False
    
    # draws everything on the screen
    pygame.display.flip()
    
pygame.quit()