"""
adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
"""
# this gets the pygame module, we can import other packages also!
import pygame
from pygame_constants import *


def center_coords(x: int, y: int, obj_width: int, obj_height: int) -> tuple[int, int]:
    """
    Adjusts the input coordinates such that the object is centered on them rather than drawn from the top left.
    :param x:
        int, desired x location
    :param y:
        int, desired y location
    :param obj_width:
        int, object's width in pixels
    :param obj_height:
        int, object's height in pixels
    :return:
        x_new, y_new, the adjusted coordinates
    """
    # TODO: Fill in the centering method here
    pass


# our main function--this runs whenever someone runs the script!
def main():

    # starts up pygame
    pygame.init()

    # this creates our screen. Try playing with the numbers inside, this controls the size of the screen.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(">.<")

    # we can load images, and for example use them in the window icon
    logo = pygame.image.load("ghost_small.png")
    pygame.display.set_icon(logo)

    # make a boolean variable controlling our game loop
    running = True

    # game clock
    clock = pygame.time.Clock()

    # position
    x = WIDTH//2
    y = HEIGHT//2

    # TODO: create velocity variable(s) with appropriate initial values
    x_vel, y_vel = (None, None)

    # block color
    block_color = RED
    toggle_ghost = False

    # game loop below
    while running:
        # pygame captures all events, this loops through them and does something with them. We only do something with
        # the QUIT event here--break out of our game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # TODO: change movement to match the snake game.
                if event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                    

        # fill the screen as white
        screen.fill(WHITE)

        # TODO: update the coordinates


        # draw the rectangle with updated coordinates
        pygame.draw.rect(screen, block_color, [x, y, 10, 10])

        # update the display
        pygame.display.update()

        # cap the update speed at 60 FPS (set in constants)
        clock.tick(FRAME_RATE)

    # ends pygame, we need to do this to prevent hanging processes!
    pygame.quit()


# this makes it so our game ONLY runs when the module is executed as the main script (like if someone double clicks it)
# the game DOES NOT run if we import the module somewhere else (like when we imported pygame above)
if __name__ == "__main__":
    # calls the main function we made above
    main()
