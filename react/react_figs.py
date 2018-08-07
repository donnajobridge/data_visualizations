import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.patches import Rectangle
import seaborn as sns


def make_layered_hist(array, condlist, condDay, colorlist):
    fig, ax = plt.subplots()
    for cond, color in zip(condlist, colorlist):
        kde=sns.kdeplot(array[cond], ax=ax, label=cond, color=color)
        ax.legend()
        ax.set_xlabel('Distance Error (pixels)')
    kde=kde.get_figure()
    kde.savefig('figs/react_kde' + condDay + '.png')
    plt.clf()
