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
    out = Image.open(fp)
    if Path(fp).suffix == ".gif":
        out = out.convert("RGB")
    return np.array(out)


def img_to_flt(img: str | Path | np.ndarray) -> np.ndarray:
    """
    Converts an RGB image to [0, 1] scaled array
    :param img: path or array
    :return: scaled image array
    """
    # TODO: implement this using [0, 1] scaling
    return img / 255


def to_greyscale(
    img: np.ndarray, weights: np.ndarray = 1 / 3 * np.ones(3)
) -> np.ndarray:
    """_summary_

    Args:
        img (np.ndarray): _description_

    Returns:
        np.ndarray: _description_
    """
    out = np.multiply(img, weights)
    out = np.sum(img, axis=2)
    return out


