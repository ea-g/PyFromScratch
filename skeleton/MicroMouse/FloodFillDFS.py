from typing import Optional

import numpy as np
import matplotlib.pyplot as plt


def show_mat(matrix: np.ndarray, title: Optional[str] = None):
    plt.matshow(matrix)
    if title:
        plt.title(title)
    plt.show()


class FloodFillDFS:
    def __init__(self, input_matrix: np.ndarray):
        self.input_matrix = input_matrix
        self.output_matrix = input_matrix.copy()

    def flood_fill(self, start: tuple, original_val, new_val, debug: bool = False, step: Optional[int] = 0):
        """
        Performs flood fill on the input_matrix

        :param start: tuple, starting coordinates (x, y)
        :param original_val: target value/color to traverse by
        :param new_val: value to change to
        :param debug: boolean, whether to show the progress of flood fill
        :param step: optional parameter for keeping track of the iteration, used with debug set to true
        :return:
        """

        # TODO: Implement flood fill using a DFS approach
        if debug:
            show_mat(self.output_matrix, f"Matrix at step {step}")

        pass


if __name__ == "__main__":
    rng = np.random.default_rng(10)
    mat = rng.integers(0, 2, (15, 15))
    ff = FloodFillDFS(mat)
    ff.flood_fill((5, 5), mat[5, 5], 3, True, 0)
