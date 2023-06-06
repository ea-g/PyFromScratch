from solutions.lesson_23_review.review_funcs import *
from collections import Counter
import matplotlib.pyplot as plt


def prob_full(arr: list[str | int | float]) -> Counter:
    # 1) get the counts of each item in the list
    counts = Counter(arr)

    # 2) turn the counts into probabilities (or relative frequencies)
    for i in counts:
        counts[i] = counts[i]/len(arr)

    return counts


def plot_top_10(probs: Counter, title: str, file: str):
    top = sorted([(k, v) for k, v in probs.items()], key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in top[:10]][::-1]
    vals = [i[1] for i in top[:10]][::-1]
    plt.barh(labels, vals)
    plt.title(title)
    plt.savefig(file)


def main():
    page = "https://en.wikipedia.org/wiki/Pikachu"
    text = get_text(page)
    # use the prob_full() function and plot_top_10() function to get the probs and plot them
    probs = prob_full(text)
    plot_top_10(probs, "Top words on Pika Wiki", "pikabar.png")


if __name__ == "__main__":
    main()
