from typing import Literal
import API
from random import choice

# note: need to have path tracking and logic for returning to start for flood fill (manhattan distance)
direction = Literal["L", "R", "B"]


class Orientation:
    def __init__(self):
        self.seq = ["N", "W", "S", "E"]
        self.cur = 0

    def left(self):
        if self.cur < (len(self.seq) - 1):
            self.cur += 1
        else:
            self.cur = 0

    def right(self):
        if self.cur > 0:
            self.cur -= 1
        else:
            self.cur = len(self.seq) - 1

    def disp(self):
        return self.seq[self.cur]


def turn(dir: direction, ort: Orientation) -> None:
    """Turns the mouse left, right, or back based on an incoming decision and updates the orientation.  

    Args:
        dir (direction): L, R, or B
        ort (Orientation): current Orientation object of the mouse
    """
    # TODO: implement turning such that given a direction to turn, you update the orientation and turn that way using the API
    if dir == "R":
        ort.right()
        API.turnRight()
    elif dir == "L":
        ort.left()
        API.turnLeft()
    else:
        ort.left()
        ort.left()
        API.turnLeft()
        API.turnLeft()


def update_position(ort: Orientation, prev_pos: tuple):
    """Updates the current position of the mouse after the last movement

    Args:
        ort (Orientation): mouse's incoming orientation
        prev_pos (tuple): mouse's previous coordinate before moving forward a step (or half step)
    """
    # TODO: update position based on orientation after turning decision and
    # assuming moving forward one full cell
    if ort.disp() == "N":
        out = (prev_pos[0], prev_pos[1] + 1)
    elif ort.disp() == "W":
        out = (prev_pos[0] - 1, prev_pos[1])
    elif ort.disp() == "E":
        out = (prev_pos[0] + 1, prev_pos[1])
    else:
        out = (prev_pos[0], prev_pos[1] - 1)
    return out


def random_turn() -> direction | None:
    """Randomly chooses a direction based on the options available

    Returns:
        direction: direction to go in-- ['L', 'R', or 'B']. Returns None if choice is forward
    """
    # TODO: randomly choose a direction based on the options of left, right, or forward
    func_dir = [API.wallLeft, API.wallRight, API.wallFront]
    dirs = ["L", "R", "F"]
    choices = []
    for f, d in zip(func_dir, dirs):
        if not f():
            choices.append(d)
        "".join(i for i in choices)
    if choices:
        out = choice(choices)
        if out != "F":
            return out
    else:
        return "B"


class FloodFillMMS:
    pass