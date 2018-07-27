import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})


def get_cxt_figs(props_tidy):
    swarmfig=sns.swarmplot(x='locs', y='prop', hue='cond',
                   data=props_tidy, palette='Pastel1')
    plt.xticks((0,1,2),['Original', 'Updated', 'New'])
    swarmfig.set_ylabel('Proportion of Responses', fontsize=20)
    swarmfig.set_xlabel('Location Selection', fontsize=20)
    swarmfig.tick_params(labelsize=16)
    # plt.title(measure, fontsize=30)
    plt.legend(fontsize=12)
    plt.gca().legend().set_title('')
    # ax = swarmfig.axes.flatten()
    # ax[0].set_title('Active')
    # ax[1].set_title('Passive')
    swarmfig._legend.text[0].set_text('Active')
    swarmfig._legend.text[1].set_text('Passive')
    # swarmfig._legend.set_title('Location')

    swarmfig=swarmfig.get_figure()
    plt.savefig('figs/loc_cond_swarm.png')
    plt.clf()

    viosplit=sns.violinplot(x='locs', y='prop', hue='cond', split=True,
    data=props_tidy[props_tidy['locs']!=3], palette='Pastel1')
    plt.xticks((0,1),['Original', 'Update'])
    plt.ylabel('Proportion of Responses')
    plt.xlabel('Location Selection')
    viosplit=viosplit.get_figure()
    viosplit.savefig('figs/cxt_viosplit.png')
    plt.clf()
