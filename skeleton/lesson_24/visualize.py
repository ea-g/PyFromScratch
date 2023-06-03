from solutions.lesson_23_review.review_funcs import *
from collections import Counter
import matplotlib.pyplot as plt


def prob_full(arr: list[str | int | float]) -> Counter:
    # 1) get the counts of each item in the list
    counts = Counter(arr)

    # 2) TODO: divide each value in the counts dictionary by the total 
    # YOUR CODE HERE

    return counts


def plot_top_10(probs: Counter, title: str, file: str):
    top = sorted([(k, v) for k, v in probs.items()], key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in top[:10]]
    vals = [i[1] for i in top[:10]]
    plt.barh(labels, vals)
    plt.title(title)
    plt.savefig(file)


def main():
    page = "https://en.wikipedia.org/wiki/Pikachu"
    text = get_text(page)
    # TODO: use the prob_full() function and plot_top_10() function to get the probs and plot them


if __name__ == "__main__":
    main()
