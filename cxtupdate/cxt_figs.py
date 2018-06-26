import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

swarm_fig=sns.factorplot(x='cxt', y='prop', hue='locs', col='cond',
               data=props_tidy[props_tidy['locs']!=3], kind='swarm', palette='Pastel1',
               legend_out=True)
swarmfig.set_ylabels('Proportion of Responses')
swarmfig.set_xlabels('Recognition Context')
ax = swarmfig.axes.flatten()
ax[0].set_title('Active')
ax[1].set_title('Passive')
swarm_fig=swarm_fig.get_figure()
swarm_fig.save_fig('cxt_loc_cond_swarm.png')

viosplit=sns.violinplot(x='locs', y='prop', hue='cond', split=True,
data=props_tidy[props_tidy['locs']!=3], palette='Pastel1')
plt.xticks((0,1),['Original', 'Update'])
plt.ylabel('Proportion of Responses')
plt.xlabel('Location Selection')
viosplit=viosplit.get_figure()
viosplit.savefig('cxt_viosplit.png')
