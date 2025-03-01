from typing import Literal
import API
from random import choice
import numpy as np
from collections import deque

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
    if choices:
        out = choice(choices)
        if out != "F":
            return out
    else:
        return "B"


def mmspos_to_mat(pos: tuple, size: int = 16) -> tuple[int]:
    """Converts a micromouse coordinate to the corresponding point in a numpy array (matrix)

    Args:
        pos (tuple): micromouse position coordinate
        size (int, Optional): size of the square grid. Defaults to 16.

    Returns:
        tuple[int]: equivalent location in a numpy array
    """
    x = pos[0]
    y = size - pos[1] - 1
    return (y, x)


class FloodFillMMS:
    def __init__(self, size: int = 16):
        self.distances = np.ones((size, size)) * -1
        self.hwalls = np.zeros((size - 1, size))
        self.vwalls = np.zeros((size, size - 1))
        self.size = size

    def calc_dist(self):
        # TODO: reset distances when recalculating
        # TODO: change the center coords to be based off of self.size
        q = deque()
        self.distances[7:9, 7:9] = 0
        q.appendleft((7, 7))
        q.appendleft((7, 8))
        q.appendleft((8, 7))
        q.appendleft((8, 8))
        while q:
            cur = q.pop()
            up_down = [(cur[0] - 1, cur[1]), (cur[0] + 1, cur[1])]
            left_right = [(cur[0], cur[1] - 1), (cur[0], cur[1] + 1)]
            # TODO: check to see if each neighbor is empty  and accessible

    # TODO: define a function to update walls
    def update_walls(self, current_location: tuple) -> None:
        pass
