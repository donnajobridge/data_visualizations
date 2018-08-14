import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})

# forget_colors = ['darkorchid', 'mediumspringgreen', 'midnightblue']

def make_layered_lineplot(arraylist, condlist, target, colorlist, phase):
    fig, ax = plt.subplots()
    for array, color, cond in zip(arraylist, colorlist, condlist):
        line=sns.lineplot(data = array, x=array.index, y=target, ax=ax,
        label=cond, color=color)
        ax.legend()
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Proportion of Viewing')
    line=line.get_figure()
    line.savefig('figs/line' + target + phase + '.png')
    plt.clf()
