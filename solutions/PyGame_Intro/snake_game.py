"""
adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
"""
# this gets the pygame module, we can import other packages also!
import pygame
import random
from pygame_constants import *


def center_coords(x: int, y: int, obj_width: int, obj_height: int) -> tuple[int | float, int | float]:
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
    x_new = x - obj_width / 2
    y_new = y - obj_height / 2
    return x_new, y_new


def touching(snake_pos, food_pos):
    xmax_snake = snake_pos[0] + SNAKE_SIZE
    xmax_food = food_pos[0] + FOOD_WIDTH
    ymax_snake = snake_pos[1] + SNAKE_SIZE
    ymax_food = food_pos[1] + FOOD_HEIGHT
    dx = min(xmax_snake, xmax_food) - max(snake_pos[0], food_pos[0])
    dy = min(ymax_snake, ymax_food) - max(snake_pos[1], food_pos[1])
    if (dx >= 0) and (dy >= 0):
        return True


def show_text(font, text="my_text", color=(0, 0, 0), x_pos=WIDTH // 2, y_pos=HEIGHT // 2, center=True):
    my_text = font.render(text, True, color)
    if center:
        x_pos, y_pos = center_coords(x_pos, y_pos, my_text.get_width(), my_text.get_height())
    screen.blit(my_text, [x_pos, y_pos])


def draw_snake(snake_list: list):
    for pos in snake_list:
        pygame.draw.rect(screen, RED, [pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE])


# our main function--this runs whenever someone runs the script!
def main():
    # make a boolean variable controlling our game loop
    running = True
    close = False

    # game clock
    clock = pygame.time.Clock()

    # position
    x = WIDTH // 2
    y = HEIGHT // 2
    food_loc = (random.randint(0, WIDTH - FOOD_WIDTH), random.randint(0, HEIGHT - FOOD_HEIGHT))

    # TODO: create velocity variable(s) with appropriate initial values
    x_vel, y_vel = (SPEED, 0)

    score = 0
    snake = list()

    # game loop below
    while running:
        while close:
            screen.fill(WHITE)
            show_text(my_font, "GAME OVER, TO RESTART-C | TO QUIT-Q", RED)
            pygame.display.update()
            sound_lose.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        close = False
                        main()
                    if event.key == pygame.K_q:
                        close = False
                        running = False

        # pygame captures all events, this loops through them and does something with them. We only do something with
        # the QUIT event here--break out of our game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # TODO: change movement to match the snake game.
                if (event.key == pygame.K_DOWN) and ((x_vel, y_vel) != (0, -SPEED)):
                    x_vel, y_vel = (0, SPEED)
                elif (event.key == pygame.K_UP) and ((x_vel, y_vel) != (0, SPEED)):
                    x_vel, y_vel = (0, -SPEED)
                elif (event.key == pygame.K_LEFT) and ((x_vel, y_vel) != (SPEED, 0)):
                    x_vel, y_vel = (-SPEED, 0)
                elif (event.key == pygame.K_RIGHT) and ((x_vel, y_vel) != (-SPEED, 0)):
                    x_vel, y_vel = (SPEED, 0)

        # fill the screen as white
        screen.fill((0, 255, 255))
        screen.blit(back, (0, 0))

        # TODO: update the coordinates
        x = x + x_vel * 1
        y = y + y_vel

        if (x > WIDTH) or (x < 0) or (y > HEIGHT) or (y < 0):
            close = True

        # draw the snake with updated coordinates
        snake.append([x, y])
        while len(snake) - 1 > score * SNAKE_SIZE:
            snake.pop(0)
        for pos in snake[:-1]:
            if [x, y] == pos:
                close = True

        draw_snake(snake)

        # draw the food
        screen.blit(food, food_loc)

        show_text(score_font, f'Score: {score}', BLACK, 10, 0, center=False)

        # update the display
        pygame.display.update()

        # check touching
        if touching((x, y), food_loc):
            food_loc = (random.randint(0, WIDTH - FOOD_WIDTH), random.randint(0, HEIGHT - FOOD_HEIGHT))
            score += 1
            sound_score.play()

        # cap the update speed at 60 FPS (set in constants)
        clock.tick(FRAME_RATE)

    # ends pygame, we need to do this to prevent hanging processes!
    pygame.quit()


# this makes it so our game ONLY runs when the module is executed as the main script (like if someone double clicks it)
# the game DOES NOT run if we import the module somewhere else (like when we imported pygame above)
if __name__ == "__main__":
    # starts up pygame
    pygame.init()

    # this creates our screen. Try playing with the numbers inside, this controls the size of the screen.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(">.<")

    # we can load images, and for example use them in the window icon
    logo = pygame.image.load("ghost_small.png")
    pygame.display.set_icon(logo)
    food = pygame.image.load("banana.png")
    back = pygame.image.load("rick2.jpg")

    # create the game's font
    my_font = pygame.font.SysFont("Arial", 30)
    score_font = pygame.font.SysFont("Arial", 18)

    # create sound effect
    sound_score = pygame.mixer.Sound('score.wav')  # 'rickroll.wav' or 'munch.wav'
    sound_lose = pygame.mixer.Sound('rickroll.wav')
    sound_lose.set_volume(0.05)

    # calls the main function we made above
    main()
