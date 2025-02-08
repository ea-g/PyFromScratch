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
    pass


def update_position(orientation: Orientation, prev_pos: tuple):
    """Updates the current position of the mouse after the last movement

    Args:
        orientation (Orientation): mouse's incoming orientation
        prev_pos (tuple): mouse's previous coordinate before moving forward a step (or half step)
    """
    # TODO: update position based on orientation after turning decision and
    # assuming moving forward one full cell
    pass


def random_turn() -> direction | None:
    """Randomly chooses a direction based on the options available

    Returns:
        direction: direction to go in-- ['L', 'R', or 'B']. Returns None if choice is forward
    """
    # TODO: randomly choose a direction based on the options of left, right, or forward
    pass


class FloodFillMMS:
    pass