import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle, Arc
from matplotlib.collections import PatchCollection
import numpy as np
import eel
from PIL import Image



def fib(n):
    """Short summary.

    Parameters
    ----------
    n : type
        Description of parameter `n`.

    Returns
    -------
    type
        Description of returned object.

    """
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def plot_fibonacci_spiral(
    number_of_squares,
    numbers=True,
    arc=True,
    cmap="Blues",
    alpha=1,
    golden_ratio=False,
    filename="plot.png",
):
    """Short summary.

    Parameters
    ----------
    number_of_squares : type
        Description of parameter `number_of_squares`.
    numbers : type
        Description of parameter `numbers`.
    arc : type
        Description of parameter `arc`.
    cmap : type
        Description of parameter `cmap`.
    alpha : type
        Description of parameter `alpha`.
    golden_ratio : type
        Description of parameter `golden_ratio`.

    Returns
    -------
    type
        Description of returned object.

    """
    fibs = list(fib(number_of_squares))
    x = 0
    y = 0
    angle = 180
    center = (x + fibs[0], y + fibs[0])
    rectangles = []
    xs, ys = [], []

    fig, ax = plt.subplots(1, figsize=(16, 16))
    for i, side in enumerate(fibs):

        rectangles.append(Rectangle([x, y], side, side))
        if numbers and i > number_of_squares - 8:
            ax.annotate(side, xy=(x + 0.45 * side, y + 0.45 * side), fontsize=14)

        if arc:
            this_arc = Arc(
                center,
                2 * side,
                2 * side,
                angle=angle,
                theta1=0,
                theta2=90,
                edgecolor="black",
                antialiased=True,
            )
            ax.add_patch(this_arc)
        angle += 90

        xs.append(x)
        ys.append(y)
        if i == 0:
            x += side
            center = (x, y + side)
        elif i == 1:
            x -= side
            y += side
            center = (x, y)
        elif i in range(2, i + 1, 4):
            x -= side + previous_side
            y -= previous_side
            center = (x + side + previous_side, y)
        elif i in range(3, i + 1, 4):
            y -= side + previous_side
            center = (x + side + previous_side, y + side + previous_side)
        elif i in range(4, i + 1, 4):
            x += side
            center = (x, y + side + previous_side)
        elif i in range(5, i + 1, 4):
            x -= previous_side
            y += side
            center = (x, y)
        previous_side = side

    col = PatchCollection(rectangles, alpha=alpha, edgecolor="black")
    try:
        col.set(array=np.asarray(range(number_of_squares + 1)), cmap=cmap)
    except ValueError:
        print(
            f" '{cmap}' is an invalid colormap, choose a valid one from "
            "https://matplotlib.org/examples/color/colormaps_reference.html"
            " - returning to default 'Blues' colormap"
        )
        col.set(array=np.asarray(range(number_of_squares + 1)), cmap="Blues")

    ax.add_collection(col)
    ax.set_aspect("equal", "box")
    ax.set_xticks([])
    ax.set_yticks([])

    xmin = np.min(xs)
    ymin = np.min(ys)
    xmax = np.max(xs) + fibs[np.argmax(xs)]
    ymax = np.max(ys) + fibs[np.argmax(ys)]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    gr = str(fibs[i] / fibs[i - 1])
    if golden_ratio:
        plt.title(r"$\varphi$ = " + gr)
    plt.tight_layout()
    plt.savefig(filename)
    image = Image.open(filename)
    image.show()


#expose this to js
@eel.expose
def main(name_of_file, fib_numb, transparency, color, remove_labels, remove_arc, show_golden_ratio):
    plot_fibonacci_spiral(
    fib_numb,
    numbers=remove_labels,
    arc=remove_arc,
    cmap=color,
    alpha=transparency,
    golden_ratio=show_golden_ratio,
    filename=name_of_file,
)
#Start ui
eel.init('ui')
eel.start('index.html', size=(400, 720))
