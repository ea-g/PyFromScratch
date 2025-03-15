from skeleton.MicroMouse.mms_helpers import FloodFillMMS

import numpy as np


def test_base():
    # TODO: write a test for flood fill working on an empty 4x4 block
    an = np.zeros((4, 4))
    an[0:4, 0] = 1
    an[0:4, 3] = 1
    an[0, 0:4] = 1
    an[3, 0:4] = 1
    an[0, 0] = 2
    an[0, 3] = 2
    an[3, 0] = 2
    an[3, 3] = 2
    ffo = FloodFillMMS(4)
    ffo.calc_dist()
    print(ffo.distances)
    assert np.all(ffo.distances == an)
