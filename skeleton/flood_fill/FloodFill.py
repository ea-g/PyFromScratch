from collections import deque
from typing import Optional
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open("mario.jpg")
mat = np.array(img)


def show_mat(matrix: np.ndarray, title: Optional[str] = None):
    plt.matshow(matrix)
    if title:
        plt.title(title)
    plt.show()


class FloodFillBFS:
    def __init__(self, input_matrix: np.ndarray, start: tuple, new_color: tuple) -> None:
        self.input_matrix = input_matrix
        self.start = start
        self.new_color = np.array(new_color, dtype=np.uint8)
        self.output_matrix = input_matrix.copy()
        self.queue = deque()
        if self.is_valid(start):
            self.queue.appendleft(start)
            self.output_matrix[start[0], start[1]] = self.new_color
        else:
            raise ValueError(f"Start coordinate, {start}, is invalid!")

    def show_start_color(self):
        show_mat(self.input_matrix[self.start[0], self.start[1], :].reshape((1, 1, 3)), "start color")

    def show_new_color(self):
        show_mat(self.new_color.reshape((1, 1, 3)), "new color")

    def is_valid(self, coord):
        pass

    def flood_fill(self, step: int = 0, debug_step: Optional[int] = None):
        # for debug!
        step += 1
        if debug_step:
            if not step % debug_step:
                show_mat(self.output_matrix, f"Matrix at step {step}")
        pass
