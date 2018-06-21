import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score



# use groupby to create df with recall, precision, f1 scores for each subject
def get_emo_scores(emo):
    sub_score_list = []
    for sub_upin, ldf in emo.groupby(['Subj','up/in']):
        sub, upin = sub_upin

        sad=ldf[ldf['affect'].isin(['l', 's'])]
        srecall=recall_score(sad['old/new'], sad['response code'])
        sprecision=precision_score(sad['old/new'], sad['response code'])
        sf1=f1_score(sad['old/new'], sad['response code'])

        hap=ldf[ldf['affect'].isin(['l', 'h'])]
        hrecall=recall_score(hap['old/new'], hap['response code'])
        hprecision=precision_score(hap['old/new'], hap['response code'])
        hf1=f1_score(hap['old/new'], hap['response code'])

        scores={'sub':sub, 'affect':'sad','up_in':upin, 'recall':srecall, 'precision':sprecision, 'f1':sf1}
        sub_score_list.append(scores)
        scores={'sub':sub, 'affect':'happy','up_in':upin, 'recall':hrecall, 'precision':hprecision, 'f1':hf1}
        sub_score_list.append(scores)

    emo_scores=pd.DataFrame(sub_score_list)
    emo_scores.set_index('sub', inplace=True)
    return emo_scores

def get_emo_wide(emo):
    sub_wide=[]
    for sub, ldf in emo.groupby(['Subj']):
        sad=ldf[ldf['affect'].isin(['s'])]
        sad_up=sad[sad['up/in'].isin(['up'])]
        sad_in=sad[sad['up/in'].isin(['in'])]

        hap=ldf[ldf['affect'].isin(['h'])]
        hap_up=hap[hap['up/in'].isin(['up'])]
        hap_in=hap[hap['up/in'].isin(['in'])]

        lure=ldf[ldf['affect'].isin(['l'])]
        lure_up=lure[lure['up/in'].isin(['up'])]
        lure_in=lure[lure['up/in'].isin(['in'])]

        sub_dict={'sub':sub, 'sad_up_hit':sad_up['accuracy'].mean(), 'sad_in_hit':sad_in['accuracy'].mean(),
              'hap_up_hit':hap_up['accuracy'].mean(), 'hap_in_hit':hap_in['accuracy'].mean(),
              'lure_up_fa':1-lure_up['accuracy'].mean(), 'lure_in_fa':1-lure_in['accuracy'].mean()}
        sub_wide.append(sub_dict)

    emo_wide=pd.DataFrame(sub_wide)
    emo_wide.set_index('sub', inplace=True)
    return emo_wide

def get_emo_tidy(emo):
    sub_tidy=[]
    for row, ldf in emo.groupby(['Subj', 'affect', 'up/in']):
        sub, affect, up_in=row
        if affect=='l':
            measure='fa'
            value=1-ldf['accuracy'].mean()
        else:
            measure='hit'
            value=ldf['accuracy'].mean()

        sub_tidy_dict={'sub':sub, 'affect':affect, 'up_in':up_in, 'measure':measure, 'value':value}
        sub_tidy.append(sub_tidy_dict)
    emo_tidy=pd.DataFrame(sub_tidy)
    return emo_tidy
