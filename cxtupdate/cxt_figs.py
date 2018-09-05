import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})


def get_cxt_figs(props_tidy):
    props_tidy['cond']=props_tidy['cond'].map({'act':'Active', 'pas':'Passive'})
    swarmfig=sns.swarmplot(x='locs', y='prop', hue='cond',
                   data=props_tidy, palette='Paired')
    plt.xticks((0,1,2),['Original', 'Updated', 'New'])
    swarmfig.set_ylabel('Proportion of Responses', fontsize=20)
    swarmfig.set_xlabel('Location Selection', fontsize=20)
    swarmfig.tick_params(labelsize=16)
    plt.legend(fontsize=12)
    plt.gca().legend().set_title('')
    swarmfig=swarmfig.get_figure()
    plt.savefig('figs/loc_cond_swarm.png')
    plt.clf()

    viosplit=sns.violinplot(x='locs', y='prop', hue='cond', split=True,
    data=props_tidy[props_tidy['locs']!=3], palette='Paired')
    plt.xticks((0,1),['Original', 'Update'])
    viosplit.set_ylabel('Proportion of Responses')
    viosplit.set_xlabel('Location Selection')
    plt.legend(fontsize=12)
    plt.gca().legend().set_title('')
    viosplit=viosplit.get_figure()
    viosplit.savefig('figs/cxt_viosplit.png')
    plt.clf()
