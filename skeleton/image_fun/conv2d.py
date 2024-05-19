import numpy as np


def conv2d(img: np.ndarray, filt: np.ndarray, pad: int = 1) -> np.ndarray:
    # TODO: implement the convolution operation (cross correlation) 
    # 1. figure out your output shape
    # 2. pad the input by pad 
    # 3. apply the filter to each pixel, we'll need to go by column (inner) and by row (outer)
    out_shape = (1, 1) # fix this!
    imgp = np.pad(img, (pad, pad))
    out = []
    pass
    return out



