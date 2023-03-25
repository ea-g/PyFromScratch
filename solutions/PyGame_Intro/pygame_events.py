"""
adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
"""
# this gets the pygame module, we can import other packages also!
import pygame
from pygame_constants import *


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

    # block color
    block_color = RED

    # show ghost?
    ghost = False

    # game loop below
    while running:
        # pygame captures all events, this loops through them and does something with them. We only do something with
        # the QUIT event here--break out of our game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # DO SOMETHING HERE
                    ghost = not ghost
                if event.key == pygame.K_DOWN:
                    y += 10
                if event.key == pygame.K_UP:
                    y -= 10
                if event.key == pygame.K_LEFT:
                    x -= 10
                if event.key == pygame.K_RIGHT:
                    x += 10
                if event.key == pygame.K_b:
                    block_color = BLACK
                if event.key == pygame.K_w:
                    block_color = WHITE
                if event.key == pygame.K_SLASH:
                    x = WIDTH // 2
                    y = HEIGHT // 2
                    block_color = RED
            
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                    

        # fill the screen as white
        screen.fill(BLACK)

        # draw a rectangle in the center
        pygame.draw.rect(screen, block_color, [x, y, 20, 20])

        # draw ghost if told to
        if ghost == True:
            screen.blit(logo.convert(), (x + 25, y - 25))
        pygame.display.update()

        # update at 60 FPS (set in constants
        clock.tick(FRAME_RATE)

    # ends pygame, we need to do this to prevent hanging processes!
    pygame.quit()


# this makes it so our game ONLY runs when the module is executed as the main script (like if someone double clicks it)
# the game DOES NOT run if we import the module somewhere else (like when we imported pygame above)
if __name__ == "__main__":
    # calls the main function we made above
    main()
