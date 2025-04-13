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


def mmspos_to_mat(pos: tuple, size: int = 16, to_mms=False) -> tuple[int]:
    """Converts a micromouse coordinate to the corresponding point in a numpy array (matrix)
    and back

    Args:
        pos (tuple): micromouse position coordinate
        size (int, Optional): size of the square grid. Defaults to 16.

    Returns:
        tuple[int]: equivalent location in a numpy array
    """
    if not to_mms:
        x = pos[0]
        y = size - pos[1] - 1

        return (y, x)
    else:
        x = pos[1]
        y = size - pos[0] - 1
        return (x, y)


class FloodFillMMS:
    def __init__(self, size: int = 16):
        self.distances = np.ones((size, size)) * -1
        self.hwalls = np.zeros((size - 1, size))
        self.vwalls = np.zeros((size, size - 1))
        self.size = size

    def calc_dist(self, mode: Literal["normal", "return"] = "normal"):
        # setup a queue
        q = deque()
        # reset distances when recalculating
        self.distances = np.ones((self.size, self.size)) * -1
        if mode == "normal":
            self.distances[
                self.size // 2 - 1 : self.size // 2 + 1,
                self.size // 2 - 1 : self.size // 2 + 1,
            ] = 0
            # add the center coords to queue
            q.appendleft((self.size // 2 - 1, self.size // 2 - 1))
            q.appendleft((self.size // 2 - 1, self.size // 2))
            q.appendleft((self.size // 2, self.size // 2 - 1))
            q.appendleft((self.size // 2, self.size // 2))
        else:
            # TODO: set the goal to 0 and add it to the queue for returning to the start
            g = mmspos_to_mat((0, 0))
            self.distances[g[0], g[1]] = 0
            q.appendleft(g)

        while q:
            cur = q.pop()
            up_down = [(cur[0] - 1, cur[1]), (cur[0] + 1, cur[1])]
            left_right = [(cur[0], cur[1] - 1), (cur[0], cur[1] + 1)]
            # check to see if each neighbor is empty  and accessible
            # add edge case checks (are neighbors valid/in bounds)
            # checking and changing up and down
            if self.in_bounds(up_down[0]):
                if (not self.hwalls[cur[0] - 1, cur[1]]) and (
                    self.distances[up_down[0][0], up_down[0][1]] < 0
                ):
                    self.distances[up_down[0][0], up_down[0][1]] = (
                        self.distances[cur[0], cur[1]] + 1
                    )
                    q.appendleft(up_down[0])
            if self.in_bounds(up_down[1]):
                if not self.hwalls[cur[0], cur[1]] and (
                    self.distances[up_down[1][0], up_down[1][1]] < 0
                ):
                    self.distances[up_down[1][0], up_down[1][1]] = (
                        self.distances[cur[0], cur[1]] + 1
                    )
                    q.appendleft(up_down[1])

            # checking and changing left and right
            if self.in_bounds(left_right[0]):
                if (not self.vwalls[cur[0], cur[1] - 1]) and (
                    self.distances[left_right[0][0], left_right[0][1]] < 0
                ):
                    self.distances[left_right[0][0], left_right[0][1]] = (
                        self.distances[cur[0], cur[1]] + 1
                    )
                    q.appendleft(left_right[0])
            if self.in_bounds(left_right[1]):
                if not self.vwalls[cur[0], cur[1]] and (
                    self.distances[left_right[1][0], left_right[1][1]] < 0
                ):
                    self.distances[left_right[1][0], left_right[1][1]] = (
                        self.distances[cur[0], cur[1]] + 1
                    )
                    q.appendleft(left_right[1])

    # TODO: make a function to check if a cell is in bounds
    def in_bounds(
        self, coord: tuple, mat: Literal["dist", "hwalls", "vwalls"] = "dist"
    ) -> bool:
        coord = np.array(coord)
        if mat == "dist":
            return np.all((coord >= 0)) and np.all((coord < self.size))
        elif mat == "hwalls":
            return (
                np.all((coord >= 0))
                and (coord[0] < self.size - 1)
                and (coord[1] < self.size)
            )
        else:
            return (
                np.all((coord >= 0))
                and (coord[0] < self.size)
                and (coord[1] < self.size - 1)
            )

    # TODO: finish the function checking whether a neighbor from 'cur' in direction 'heading' is accessible
    def is_accessible(self, coord: tuple, heading: Literal["N", "S", "W", "E"]) -> bool:
        """Determines if a neighboring cell of a particular coordinate in a given direction is accessible.

        Args:
            coord (tuple): a given location in the distance matrix
            heading (str): direction from the coord to check accessibility

        Returns:
            bool: whether the cell in a given heading is accessible from coord
        """
        if heading == "N":
            return not self.hwalls[coord[0] - 1, coord[1]]
        elif heading == "S":
            return not self.hwalls[coord[0], coord[1]]
        elif heading == "W":
            return not self.vwalls[coord[0], coord[1] - 1]
        else:
            return not self.vwalls[coord[0], coord[1]]

    # TODO: define a function to update walls
    def update_walls(self, current_location: tuple, ort: Orientation) -> None:
        walls = dict()
        # change mms coordinate to matrix style
        pos = mmspos_to_mat(current_location, self.size)
        if ort.disp() == "N":
            walls["left"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1] - 1)
                if self.in_bounds((pos[0], pos[1] - 1), "vwalls")
                else None,
            }  # note that we check if the wall is in bounds, TODO: double check in bounds part
            walls["right"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "vwalls")
                else None,
            }
            walls["front"] = {
                "wall": self.hwalls,
                "coord": (pos[0] - 1, pos[1])
                if self.in_bounds((pos[0] - 1, pos[1]), "hwalls")
                else None,
            }
            walls["back"] = {
                "wall": self.hwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "hwalls")
                else None,
            }
            dir_to_heading = {"left": "w", "right": "e", "front": "n", "back": "s"}
        elif ort.disp() == "S":
            # TODO: fill in S, W, and E versions of which walls are left, right, front, and back
            walls["left"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "vwalls")
                else None,
            }
            walls["right"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1] - 1)
                if self.in_bounds((pos[0], pos[1] - 1), "vwalls")
                else None,
            }
            walls["front"] = {
                "wall": self.hwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "hwalls")
                else None,
            }
            walls["back"] = {
                "wall": self.hwalls,
                "coord": (pos[0] - 1, pos[1])
                if self.in_bounds((pos[0] - 1, pos[1]), "hwalls")
                else None,
            }
            dir_to_heading = {"left": "e", "right": "w", "front": "s", "back": "n"}
        elif ort.disp() == "E":
            walls["back"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1] - 1)
                if self.in_bounds((pos[0], pos[1] - 1), "vwalls")
                else None,
            }  #
            walls["front"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "vwalls")
                else None,
            }
            walls["left"] = {
                "wall": self.hwalls,
                "coord": (pos[0] - 1, pos[1])
                if self.in_bounds((pos[0] - 1, pos[1]), "hwalls")
                else None,
            }
            walls["right"] = {
                "wall": self.hwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "hwalls")
                else None,
            }
            dir_to_heading = {"left": "n", "right": "s", "front": "e", "back": "w"}
        else:
            walls["front"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1] - 1)
                if self.in_bounds((pos[0], pos[1] - 1), "vwalls")
                else None,
            }
            walls["back"] = {
                "wall": self.vwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "vwalls")
                else None,
            }
            walls["right"] = {
                "wall": self.hwalls,
                "coord": (pos[0] - 1, pos[1])
                if self.in_bounds((pos[0] - 1, pos[1]), "hwalls")
                else None,
            }
            walls["left"] = {
                "wall": self.hwalls,
                "coord": (pos[0], pos[1])
                if self.in_bounds((pos[0], pos[1]), "hwalls")
                else None,
            }
            dir_to_heading = {"left": "s", "right": "n", "front": "w", "back": "e"}
        # TODO: change the value of the wall from 0 to 1 if there is a wall there
        for w, val in zip(
            sorted(walls.keys()),
            [API.wallBack, API.wallFront, API.wallLeft, API.wallRight],
        ):
            if val() and walls[w]["coord"]:
                # make pointers to the correct wall matrix and coordinate
                wall = walls[w]["wall"]
                coord = walls[w]["coord"]
                # set each discovered wall to 1 in their matrix
                wall[coord[0], coord[1]] = 1
                # show the wall as discovered on the simulator
                API.setWall(current_location[0], current_location[1], dir_to_heading[w])

    # TODO: define a function to determine where to turn based on distance matrix, current location, and orientation
    # will need to get goal and possibly recalculate distance with floodfill
    def prep_move(
        self,
        current_location: tuple,
        ort: Orientation,
        mode: Literal["normal", "return"],
    ) -> None:
        pos = mmspos_to_mat(current_location, self.size)
        # Steps:
        # 1) get accessible and lower dist neighbors
        # 2) if none, calc dist and repeat from (1)
        # 3) turn toward the lowest distance neighbor
        redo = True
        # prepare each neighbor and its corresponding heading
        headings = ["N", "W", "S", "E"]
        neighbors = [
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] + 1),
        ]
        while redo:
            # TODO: perform step 1--find which neigbors are accessible and have a distance value lower
            # than the current position's distance value.
            # If these conditions are met, add the neighbor's distance and heading direction to a list
            current_distance = self.distances[pos[0], pos[1]]  # TODO: fill me in
            n_dists = []
            n_heads = []
            for h, n in zip(headings, neighbors):
                if self.in_bounds(n):
                    neighb_dist = self.distances[
                        n[0], n[1]
                    ]  # TODO: fill me in with the neighbor's distanct (n)
                    # TODO: finish up step 1
                    if neighb_dist < current_distance and self.is_accessible(pos, h):
                        n_dists.append(neighb_dist)
                        n_heads.append(h)
            if n_heads:
                redo = False
            else:
                # TODO: implement step 2 here
                self.calc_dist(mode=mode)
        # TODO: implement step 3--turn toward the lowest distance neighbor
        # get the heading of the lowest distance neighbor
        target_heading = n_heads[np.argmin(n_dists)]
        # TODO: figure out the number of turns it would take to reorient from
        # the current orientation to the target heading
        # based on the number of turns required, turn the mouse in a direction (back: 'B', left: 'L', or right:'R')
        turns = headings.index(ort.disp()) - headings.index(target_heading)
        if turns:
            if turns in (-3, 1):
                turn("R", ort=ort)
            elif abs(turns) == 2:
                turn("B", ort=ort)
            else:
                turn("L", ort=ort)
