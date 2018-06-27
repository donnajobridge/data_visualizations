import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_cxt_figs(props_tidy):
    swarmfig=sns.factorplot(x='cxt', y='prop', hue='locs', col='cond',
                   data=props_tidy[props_tidy['locs']!=3], kind='swarm', palette='Pastel1',
                   legend_out=True)
    plt.xticks((0,1),['Familiar', 'Novel'])
    swarmfig.set_ylabels('Proportion of Responses')
    swarmfig.set_xlabels('Recognition Context')
    ax = swarmfig.axes.flatten()
    ax[0].set_title('Active')
    ax[1].set_title('Passive')
    swarmfig._legend.texts[0].set_text('Original')
    swarmfig._legend.texts[1].set_text('Updated')
    swarmfig._legend.set_title('Location')

    # swarmfig=swarmfig.get_figure()
    plt.savefig('figs/cxt_loc_cond_swarm.png')
    plt.clf()

    viosplit=sns.violinplot(x='locs', y='prop', hue='cond', split=True,
    data=props_tidy[props_tidy['locs']!=3], palette='Pastel1')
    plt.xticks((0,1),['Original', 'Update'])
    plt.ylabel('Proportion of Responses')
    plt.xlabel('Location Selection')
    viosplit=viosplit.get_figure()
    viosplit.savefig('figs/cxt_viosplit.png')
    plt.clf()
