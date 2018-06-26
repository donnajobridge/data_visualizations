import matplotlib.pyplot as plt
import seaborn as sns

def make_layered_hist(array, condlist, condDay):
    fig, ax = plt.subplots()
    for cond in condlist:
        hist_kde=sns.distplot(array[cond], ax=ax, label=cond)
        ax.legend()
        ax.set_xlabel('Distance Error (pixels)')
        hist_kde=hist_kde.get_figure()
        hist_kde.savefig('figs/react_hist_kde' + condDay + '.png')
