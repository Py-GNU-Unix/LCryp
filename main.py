import argparse
import unidecode
import matplotlib
import matplotlib.pyplot as plt
from decimal import Decimal
from stats import italian_letters_stats

matplotlib.use("QtAgg")


def main():
    parser = argparse.ArgumentParser(description="Calculate chipher text statistics")
    parser.add_argument("-infile", type=argparse.FileType("r"))
    parser.add_argument("--include-unalpha", action="store_true")

    args = parser.parse_args()
    
    if args.infile:
        stats = create_stats(args)
        figure, axis = plt.subplots(1, 2)

        plot_text_stats(stats, axis[0])
        plot_lang_stats(italian_letters_stats, axis[1])
    else:
        figure, axis = plt.subplots(1,1)
        plot_lang_stats([(a,b) for a,b in italian_letters_stats if a and b], axis)

    plt.show()


def create_stats(args):
    stats = {}
    lenght = 0
    last_char = ""

    for char in args.infile.read():
        char = unidecode.unidecode(char)

        if char.isalpha() or args.include_unalpha:
            char = char.lower()

            if char in stats:
                stats[char]["count"] += 1

                if last_char == char:
                    stats[char]["double"] = True

            else:
                stats.update({char: {"count": 1, "double": False}})

            last_char = char
            lenght += 1

    for char in stats:
        stats[char]["perc"] = Decimal(
            str(stats[char]["count"] / lenght * 100)
        ).quantize(Decimal(".1"))

    return stats


def plot_text_stats(stats, plt):

    vals = sorted(
        zip([L["perc"] for L in stats.values()], stats.keys()),
        key=lambda x: x[0],
        reverse=True,
    )

    plot_data(vals, plt)


def plot_lang_stats(lang, plt):

    vals = sorted(
        zip(map(lambda L: L[1], lang), map(lambda L: L[0], lang)),
        key=lambda x: x[0],
        reverse=True,
    )

    plot_data(vals, plt)


def plot_data(vals, plt):

    height = list(map(lambda x: x[0], vals))
    tick_label = list(map(lambda x: x[1], vals))

    columns = list(range(len(list(height))))
    plt.bar(columns, height, tick_label=tick_label, width=0.9)

    for i in columns:
        plt.text(i, height[i] / 2, height[i], ha="center", size=10)


main()
