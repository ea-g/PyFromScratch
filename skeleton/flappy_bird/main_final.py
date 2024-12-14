import pygame
from sys import exit
from types import SimpleNamespace
from pathlib import Path
from flappy_dtypes import Node, CircularList
from random import randint

# start pygame
pygame.init()
# used for controlling framerate
clock = pygame.time.Clock()

# window, size of background image
HEIGHT = 720
WIDTH = 551
window = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0
# Game Constants
SCROLL_SPEED = 1  # Set scroll speed of the game
# game font
font = pygame.font.SysFont("Segoe", 26)


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
    def __init__(  # TODO: add flap_power, and attribute for if we can control
        self,
        x,
        y,
        imgs: CircularList,
        gravity,
        terminal_vel=7,
        ground_y=520,
        flap_power=3,
        *groups,
    ):
        super().__init__(*groups)
        # properties of the class, similar to ground
        self.cur_img = imgs.last  # Node of our linked
        self.image = self.cur_img.data  #  pygame surface
        self.rect = self.image.get_rect()  # fill in
        self.rect.x, self.rect.y = x, y  # fill in
        self.gravity = gravity
        self.y_vel = 0  # our starting velocity moving up and down
        self.terminal_vel = terminal_vel  # fastest we will drop or rise
        self.ground_y = ground_y
        self.flap_power = flap_power
        self.control = True  # attribute for if we can control

    def update(self, user_inp: dict):  # add an argument for user input
        if self.control:
            # wrap in control attribute
            # define how the bird updates
            self.y_vel += (
                self.gravity
            )  # adjust the fall velocity, remember this updates each frame
            # adjust the falling vel by flap power if user input and animate
            if user_inp.get("mouse")[0] or user_inp.get("key")[pygame.K_SPACE]:
                self.y_vel -= self.flap_power

                # update the display graphics
                self.cur_img = self.cur_img.next
                self.image = self.cur_img.data

            # readjust the fall to the max
            # adjust this to deal with flap power
            if abs(self.y_vel) > self.terminal_vel:
                if self.y_vel > 0:
                    self.y_vel = self.terminal_vel
                else:
                    self.y_vel = -self.terminal_vel  # fill me in

            # adjust the position of the bird by the velocity (pixels per frame), use self.rect.y for the position of the bird
            self.rect.y += self.y_vel

            # where should the bird be if it hits the ground? use self.rect.bottom to get the bottom of the bird
            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y + 1  # adjust to allow colision

            if self.rect.top < 0:
                self.rect.top = 0

            # rotate the image by some velocity factor so bird faces in right direction pygame.transform.rotate(im, degree) hint: use cur_img.data not self.image
            self.image = pygame.transform.rotate(
                self.cur_img.data, self.y_vel * -7
            )  # fill me in


# TODO: make the pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y:int, img, scroll_speed:int , pipe_type:str, sound=None, *groups
    ):  # TODO: add sound for the score (you'll need an argument!)
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y  # the position of our pipe
        self.scroll_speed = scroll_speed
        self.pipe_type = pipe_type
        self.sound = sound

    def update(self):
        # TODO: move the pipe
        self.rect.x -= self.scroll_speed
        if self.rect.x <= (0 - self.image.get_width()):
            self.kill()
            
        # TODO: fix problem here
        global score
        if (self.rect.x == (WIDTH//3 - self.image.get_width())) and (self.pipe_type == "bottom"):
            score += 1
            # TODO: add sound effect! use pygame.mixer.Sound.play
            pygame.mixer.Sound.play(self.sound)


def load_assets(fldr: Path) -> SimpleNamespace:
    """Loads all assets (images/sounds) from a folder and creates a simple namespace of them.

    Args:
        fldr (Path): Path to the assets folder

    Returns:
        SimpleNamespace: SimpleNamespace with a pygame Surface per asset as each attribute
    """
    # load assets into a dictionary and change to simplenamespace
    out = {}
    for i in fldr.iterdir():
        if i.suffix == ".png":
            out[i.stem] = pygame.image.load(i)
        if i.suffix in (".wav", ".mp3"):
            if "music" in i.stem:
                pygame.mixer.music.load(i)
            else:
                out[i.stem] = pygame.mixer.Sound(i)
    return SimpleNamespace(**out)


# look for quit event and end game
def end_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# main game function
def main(assets):
    global score

    # initialize the ground
    x_ground, y_ground = 0, 520
    ground = pygame.sprite.Group()  # to contain many ground pieces
    pipes = pygame.sprite.Group()
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
    # TODO: add start screen loop here, flip run to true after start button

    # use bird.add to add our Bird sprite to the group
    # adjust flap_power when initializing bird
    bird.add(Bird(x_bird, y_bird, bird_imgs, 0.5, 7, flap_power=1))
    pipe_timer = 0
    while run:
        # look for quit event
        end_game()

        # reset frame with black screen
        window.fill((0, 0, 0))

        # Capture user input here into a dict (pygame.key/mouse)
        user_input = dict(
            key=pygame.key.get_pressed(), mouse=pygame.mouse.get_pressed()
        )  # fill me in
        # Draw the background here (can use blit)
        window.blit(assets.background, (0, 0))

        # spawn ground here (add Ground pieces to the ground group)
        if len(ground) < 2:
            ground.add(Ground(WIDTH, y_ground, assets.ground, SCROLL_SPEED))

        # Draw ground, pipes, etc here (use obj.draw(surface))
        # TODO: draw the pipes, think about ordering...
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # TODO: draw the score here
        score_text = font.render(f"Score: {score}", True, (255, 255, 255)) # TODO use font.render() to make a score text
        # TODO: blit the window with the score text
        window.blit(score_text, (25, 25))

        # update ground, pipes, bird, etc here
        # TODO: edit the update to account for if still playing
        if bird.sprite.control:
            pipes.update()
            ground.update()
            bird.update(user_input)  # add user input to the update

        # TODO: collision detection here and logic (use the control attribute), pygame.sprite.spritecollide
        if pygame.sprite.spritecollide(bird.sprite, ground, False) or pygame.sprite.spritecollide(bird.sprite, pipes, False):
            bird.sprite.control = False
            # TODO: add gameover here
            window.blit(assets.game_over, (WIDTH//2 - assets.game_over.get_width()//2, HEIGHT//2 - assets.game_over.get_height()//2))
            if user_input.get("key")[pygame.K_r]:
                score = 0
                break

        # TODO: spawn pipes here, use a time interval between 180 and 250 frames for new pipes
        
        if pipe_timer <= 0 and bird.sprite.control:
            tp_y = -assets.pipe_top.get_height() + 50
            tp_yb = -assets.pipe_top.get_height() + y_ground - 50 - assets.bird_up.get_height() - 150
            toppipe_y = randint(tp_y, tp_yb)
            bp_y = toppipe_y + assets.pipe_top.get_height() + assets.bird_up.get_height() + randint(50, 300) # TODO: fix this
            bp_y = min(bp_y, y_ground - 50)
            pipe_x = WIDTH
            pipes.add(Pipe(pipe_x, toppipe_y, assets.pipe_top, SCROLL_SPEED, "top"))
            pipes.add(Pipe(pipe_x, bp_y, assets.pipe_bottom, SCROLL_SPEED, "bottom", assets.score))
            pipe_timer = randint(180, 250)
        pipe_timer -= 1
        
        

        clock.tick(60)  # frame rate refresh
        pygame.display.update()  # update the frame
    
def start_game():
    assets = load_assets(Path("./skeleton/flappy_bird/assets"))
    pygame.mixer.music.play(-1)
    while True:
        end_game()
        window.blit(assets.background, (0, 0))
        window.blit(assets.ground, (0, 520))
        window.blit(assets.start, (WIDTH//2 - assets.start.get_width()//2, HEIGHT//2 - assets.start.get_height()//2))
        window.blit(assets.bird_mid, (WIDTH // 3, HEIGHT // 4))
        
        user_inp = dict(
            key=pygame.key.get_pressed(), mouse=pygame.mouse.get_pressed()
        )
        if user_inp.get("mouse")[0] or user_inp.get("key")[pygame.K_SPACE]:
            main(assets)
            
        pygame.display.update()


if __name__ == "__main__":
    start_game()
