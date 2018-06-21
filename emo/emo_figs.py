import seaborn as sns
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def emo_confusion(emo, affect_code):
    orient=['up', 'in']
    for up_in in orient:
        affect=emo[emo['affect'].isin(['l', 's'])]
        up_in_affect=affect[affect['up/in']==up_in]

        cm=confusion_matrix(up_in_affect['old/new'], up_in_affect['response code'])
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cmfig=sns.heatmap(cm, cmap='Blues', annot=True, fmt='g')
        plt.title(affect_code+'_'+ up_in)
        cmfig=cmfig.get_figure()
        fname='figs/emo_cm_' + up_in + '_' + affect_code + '.png'
        cmfig.savefig(fname)
        plt.clf()

def make_bar(emo_scores, measure):
    bar=sns.barplot(x='up_in', y=measure, hue='affect', data=emo_scores, palette='Set2')
    plt.title(measure)
    barfig=bar.get_figure()
    barfig.savefig('figs/emo_bar_'+measure+'.png')
    plt.clf()
