import API
import sys
from mms_helpers import Orientation


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "*")
    ort = Orientation()
    coord = (0, 0)
    while True:
        log(ort.disp())
        # TODO: implement the logic of your mouse including turning, choosing, moving, and keeping track of the position (not necessarily in that order...)
        # you can move forward using API.moveForward()

        # setting color for cells we've traversed
        API.setColor(*coord, color="b")  # choose your color
        # stop if we've reached the goal!
        if coord[0] in (7, 8) and coord[1] in (7, 8):
            break


if __name__ == "__main__":
    main()
