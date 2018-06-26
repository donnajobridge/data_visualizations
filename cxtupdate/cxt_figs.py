import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

swarm_fig=sns.factorplot(x='cxt', y='prop', hue='locs', col='cond',
               data=props_tidy[props_tidy['locs']!=3], kind='swarm', palette='Pastel1')
swarm_fig=swarm_fig.get_figure()
swarm_fig.save_fig('cxt_loc_cond_swarm.png')
