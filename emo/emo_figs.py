import seaborn as sns
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def emo_confusion(emo):
    for emotion in ['h', 's']:
        for up_in in ['up', 'in']:
            affect=emo[emo['affect'].isin(['l', emotion])]
            up_in_affect=affect[affect['up/in']==up_in]
            cm=confusion_matrix(up_in_affect['old/new'], up_in_affect['response code'])
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

            cmfig=sns.heatmap(cm, cmap='Blues', annot=True, fmt='g', vmin=0, vmax=.8)
            plt.title(emotion+'_'+ up_in)
            cmfig=cmfig.get_figure()
            fname='figs/emo_cm_' + up_in + '_' + emotion + '.png'
            cmfig.savefig(fname)
            plt.clf()

def make_bar(emo_scores):
    for measure in ['f1', 'precision', 'recall']:
        bar=sns.barplot(x='up_in', y=measure, hue='affect', data=emo_scores, palette='Set2')
        plt.title(measure)
        barfig=bar.get_figure()
        barfig.savefig('figs/emo_bar_'+measure+'.png')
        plt.clf()

def make_line(emo_scores):
    for measure in ['f1', 'precision', 'recall']:
        line=sns.pointplot(x='up_in', y=measure, hue='affect', jitter=True, data=emo_scores, palette='Set2')
        plt.title(measure)
        linefig=line.get_figure()
        linefig.savefig('figs/emo_line_'+measure+'.png')
        plt.clf()
