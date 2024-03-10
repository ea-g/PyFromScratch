from PIL import Image
import numpy as np
import skimage as ski
from pathlib import Path


def load_im_arr(fp: str | Path) -> np.ndarray:
    """
    Loads an image from file into a numpy array

    :param fp: file path
    :return: image as numpy array
    """
    return np.array(Image.open(fp))


def img_to_flt(img: str | Path | np.ndarray) -> np.ndarray:
    """
    Converts an RGB image to [0, 1] scaled array
    :param img: path or array
    :return: scaled image array
    """
    # TODO: implement this using [0, 1] scaling
    pass


def to_greyscale(img: np.ndarray) -> np.ndarray:
    """
    Converts an RGB image in floating point to a greyscale representation
    :param img:
    :return: greyscale image
    """
    pass