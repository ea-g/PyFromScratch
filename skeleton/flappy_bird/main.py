import pygame
from sys import exit
from types import SimpleNamespace
from pathlib import Path

# start pygame
pygame.init()
# used for controlling framerate
clock = pygame.time.Clock()

# window
HEIGHT= 720
WIDTH = 551
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Constants
SCROLL_SPEED = 1 # Set scroll speed of the game

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, img, scroll_speed):
        super().__init__()
        # TODO: define the properties of the class, note that we're making ground a rectangle sprite with the image in it
        
        
    def update(self):
        # TODO: move the ground using the rectangle, delete it if it's outside the window 
        pass

def load_assets(fldr: Path) -> SimpleNamespace:
    """Loads all assets (images) from a folder and creates a simple namespace of them.

    Args:
        fldr (Path): _description_

    Returns:
        SimpleNamespace[pygame.Surface]: _description_
    """
    # TODO: fill in code here
    pass


# look for quit event and end game
def end_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
# main game function
def main():
    # TODO: initialize the ground here
    x_ground, y_ground = 0, 520
    ground = pygame.sprite.Group() # to contain many ground pieces
    # TODO: add Grounds to the ground group
    
    run = True
    while run:
        # look for quit event
        end_game()
        
        # reset frame with black screen
        window.fill((0, 0, 0))
        # TODO: Draw the background here (can use blit)
        
        # TODO: spawn ground here (add Ground pieces to the ground group)
            
        
        # TODO: Draw ground, pipes, etc here (use obj.draw(surface))
        
        # TODO: update ground, pipes, etc here
        ground.update()
        clock.tick(60) # frame rate refresh
        pygame.display.update() # update the frame
             
main()