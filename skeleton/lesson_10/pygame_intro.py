"""
adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
"""
# this gets the pygame module, we can import other packages also!
import pygame


# our main function--this runs whenever someone runs the script!
def main():

    # starts up pygame
    pygame.init()

    # this creates our screen. Try playing with the numbers inside, this controls the size of the screen.
    width = 800
    height = 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("What should your window be called??")
    # we can load images, and for example use them in the window icon
    logo = pygame.image.load("ghost_small.png")
    pygame.display.set_icon(logo)

    # make a boolean variable controlling our game loop
    running = True

    # game loop below
    while running:
        # pygame captures all events, this loops through them and does something with them. We only do something with
        # the QUIT event here--break out of our game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # ends pygame, we need to do this to prevent hanging processes!
    pygame.quit()


# this makes it so our game ONLY runs when the module is executed as the main script (like if someone double clicks it)
# the game DOES NOT run if we import the module somewhere else (like when we imported pygame above)
if __name__ == "__main__":
    # calls the main function we made above
    main()
