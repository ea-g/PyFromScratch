import API
import sys
from mms_helpers import Orientation, random_turn, turn, update_position, FloodFillMMS


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "*")
    ort = Orientation()
    coord = (0, 0)
    ffo = FloodFillMMS()
    # initialize the distance matrix
    ffo.calc_dist()
    # set the mode to normal (going to center) to start
    mode = "normal"
    while True:
        # TODO: implement the logic of your mouse including choosing, moving, turning, keeping track of the position, and walls 
        # (not necessarily in that order...)
        # you can move forward using API.moveForward()
        ffo.update_walls(coord, ort)
        ffo.prep_move(coord, ort, mode)
        API.moveForward()
        coord = update_position(ort, coord)
        # setting color for cells we've traversed
        API.setColor(*coord, color="Y")  # choose your color
        # TODO: stop or go back to the beginning if we've reached the goal!
        if coord[0] in (7, 8) and coord[1] in (7, 8):
            mode = "return"
        if coord == (0, 0):
            mode = "normal"


if __name__ == "__main__":
    main()
