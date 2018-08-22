import seaborn as sns
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})

def make_rencode_figs(dprimedf, measure_array, conf):
    # for fig_type, myplot in [('bar', sns.barplot), ('swarm', sns.swarmplot),
    # ('box', sns.boxplot)]:
    for fig_type, myplot in [('swarm', sns.swarmplot), ('box', sns.boxplot)]:
        for measure in measure_array:
            ax=myplot(x='cond', y=measure,
            data=dprimedf, palette="colorblind")
            ax.set_xlabel('Condition', fontsize=20)
            ax.tick_params(labelsize=16)
            plt.legend(fontsize=12)
            plt.gca().legend().set_title('')
            ax.set_ylabel(measure, fontsize=20)
            plt.title('Recognition Performance', fontsize=30)
            fig=ax.get_figure()
            fig.savefig('figs/rencode_'+fig_type+measure+conf+'.png')
            plt.clf()

def make_cm_matrix(rencode):
    for cond, ldf in rencode.groupby('cond'):
        trialtype = ldf['old/new']
        resp = ldf['recog_answer']
        cm=confusion_matrix(trialtype, resp)
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cmfig = sns.heatmap(cm, cmap='Blues', annot=True, fmt='g', vmin=0, vmax=.8)
        plt.title(cond)
        cmfig = cmfig.get_figure()
        fname = 'figs/rencode_cm_.png'
        cmfig.savefig(fname)
        plt.clf()
