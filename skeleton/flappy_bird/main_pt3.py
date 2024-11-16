import pygame
from sys import exit
from types import SimpleNamespace
from pathlib import Path
from flappy_dtypes import Node, CircularList

# start pygame
pygame.init()
# used for controlling framerate
clock = pygame.time.Clock()

# window, size of background image
HEIGHT = 720
WIDTH = 551
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Constants
SCROLL_SPEED = 1  # Set scroll speed of the game


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, img, scroll_speed, *groups):
        super().__init__(*groups)
        # define the properties of the class, note that we're using the rectangle property of the ground "surface" and moving it around
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y  # the position of our ground!
        self.scroll_speed = scroll_speed

    def update(self):
        # move the ground using the rectangle, delete it if it's outside the window
        self.rect.x -= self.scroll_speed
        if self.rect.x <= -WIDTH:
            self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(#TODO: add flap_power, and attribute for if we can control
        self, x, y, imgs: CircularList, gravity, terminal_vel=7, ground_y=520, *groups
    ):
        super().__init__(*groups)
        # properties of the class, similar to ground
        self.cur_img = (
            imgs.last
        )  # Node of our linked
        self.image = (
            self.cur_img.data
        )  #  pygame surface
        self.rect = self.image.get_rect()  # fill in
        self.rect.x, self.rect.y = x, y  # fill in
        self.gravity = gravity
        self.y_vel = 0  # our starting velocity moving up and down
        self.terminal_vel = terminal_vel  # fastest we will drop or rise
        self.ground_y = ground_y
        self.flap_power=None # TODO: fill me in
        # TODO: add in attribute for if we can control

    def update(self): # TODO: add an argument for user input 
        # TODO: wrap in control attribute
        # define how the bird updates
        self.y_vel += (
            self.gravity
        )  # adjust the fall velocity, remember this updates each frame
        # TODO: adjust the falling vel by flap power if user input and animate
 
        # update the display graphics
        self.cur_img = self.cur_img.next  
        self.image = self.cur_img.data
        
        
        # readjust the fall to the max 
        # TODO: adjust this to deal with flap power
        if abs(self.y_vel) > self.terminal_vel:
            if self.y_vel > 0:
                self.y_vel = self.terminal_vel
            else:
                pass # fill me in 

        # adjust the position of the bird by the velocity (pixels per frame), use self.rect.y for the position of the bird
        self.rect.y += self.y_vel

        # where should the bird be if it hits the ground? use self.rect.bottom to get the bottom of the bird
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y + 1 # adjust to allow colision
            
        # TODO: rotate the image by some velocity factor so bird faces in right direction pygame.transform.rotate(im, degree) hint: use cur_img.data not self.image
        # self.image = None # fill me in

        


def load_assets(fldr: Path) -> SimpleNamespace:
    """Loads all assets (images) from a folder and creates a simple namespace of them.

    Args:
        fldr (Path): Path to the assets folder

    Returns:
        SimpleNamespace: SimpleNamespace with a pygame Surface per asset as each attribute
    """
    # load assets into a dictionary and change to simplenamespace
    out = {}
    for i in fldr.iterdir():
        out[i.stem] = pygame.image.load(i)
    return SimpleNamespace(**out)


# look for quit event and end game
def end_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# main game function
def main():
    assets = load_assets(Path("./skeleton/flappy_bird/assets"))
    # initialize the ground
    x_ground, y_ground = 0, 520
    ground = pygame.sprite.Group()  # to contain many ground pieces
    # add Ground piece to the ground group
    ground.add(Ground(x_ground, y_ground, assets.ground, SCROLL_SPEED))
    run = True
    # initialize the bird similar to the ground
    bird = pygame.sprite.GroupSingle()
    x_bird, y_bird = WIDTH // 3, HEIGHT // 4  # pick a start location
    bird_imgs = (
        CircularList()
    )  # fill this in using the circular list, and add all the bird images to it
    bird_imgs.enter(assets.bird_down)
    bird_imgs.enter(assets.bird_mid)
    bird_imgs.enter(assets.bird_up)
    bird_imgs.enter(assets.bird_mid)

    # use bird.add to add our Bird sprite to the group
    # TODO: adjust flap_power when initializing bird
    bird.add(Bird(x_bird, y_bird, bird_imgs, 0.5, 7))
    while run:
        # look for quit event
        end_game()

        # reset frame with black screen
        window.fill((0, 0, 0))

        # TODO: Capture user input here into a dict (pygame.key/mouse)
        user_input = None # fill me in
        # Draw the background here (can use blit)
        window.blit(assets.background, (0, 0))

        # spawn ground here (add Ground pieces to the ground group)
        if len(ground) < 2:
            ground.add(Ground(WIDTH, y_ground, assets.ground, SCROLL_SPEED))

        # Draw ground, pipes, etc here (use obj.draw(surface))
        ground.draw(window)
        bird.draw(window)

        # update ground, pipes, bird, etc here
        ground.update()
        bird.update() # TODO: add user input to the update
        
        # TODO: collision detection here and logic (use the control attribute), pygame.sprite.spritecollide

        clock.tick(60)  # frame rate refresh
        pygame.display.update()  # update the frame


if __name__ == "__main__":
    main()