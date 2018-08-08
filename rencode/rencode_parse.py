import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_score, recall_score, f1_score


def get_props_tidy_all(rencode):
    type_dict = {0:'hit', 1:'fa'}
    cond_dict = {'active':'Active', 'passive':'Passive'}
    props_list = []
    for row, ldf in rencode.groupby(by=['sub', 'cond', 'old/new']):
        sub, cond, old_new = row
        count = ldf['accuracy'].count()
        prop_correct = ldf['accuracy'].sum()/count
        if old_new == 1:
            prop_correct = 1-prop_correct

        sub_dict = {'sub':sub, 'cond':cond_dict[cond], 'trialtype':type_dict[old_new], 'prop':prop_correct, 'count':count}
        props_list.append(sub_dict)
    propsdf = pd.DataFrame(props_list)
    return propsdf

def get_props_tidy_highconf(rencode):
    type_dict = {0:'hit', 1:'fa'}
    cond_dict = {'active':'Active', 'passive':'Passive'}
    props_list = []
    for row, ldf in rencode.groupby(by=['sub', 'cond', 'old/new', 'recog confidence']):
        sub, cond, old_new, conf = row
        if conf != 'high':
            continue
        count = ldf['accuracy'].count()
        prop_correct = ldf['accuracy'].sum()/count
        if old_new == 1:
            prop_correct = 1-prop_correct

        sub_dict = {'sub':sub, 'cond':cond_dict[cond], 'trialtype':type_dict[old_new], 'prop':prop_correct, 'count':count}
        props_list.append(sub_dict)
    propsdf_high = pd.DataFrame(props_list)
    return propsdf_high

def get_dprime(propsdf, Z):
    for ind, row in propsdf.iterrows():
        halfprop = .5/row['count']
        if row['prop'] == 1:
            propsdf.loc[ind,'adjusted_prop'] = 1-halfprop
        elif row['prop'] == 0:
            propsdf.loc[ind,'adjusted_prop'] = halfprop
        else: propsdf.loc[ind,'adjusted_prop'] = row['prop']
    dprimedf = propsdf.pivot_table(index=['sub','cond'],
                              columns='trialtype')['adjusted_prop'].reset_index()
    dprimedf['dprime'] = Z(dprimedf['hit']) - Z(dprimedf['fa'])
    return dprimedf

def get_score_data(rencode):
    score_list = []
    for row, ldf in rencode.groupby(by=['sub','cond']):
        sub, cond = row
        scores = {}
        trialtype = ldf['old/new']
        resp = ldf['recog_answer']

        score_funcs = [('recall', recall_score), ('precision', precision_score), ('f1', f1_score)]
        for fun_name, fun in score_funcs:
            score = fun(trialtype, resp)
            scores[fun_name] = score
        scores['cond'] = cond
        scores['sub'] = sub
        score_list.append(scores)
    scoresdf=pd.DataFrame(score_list)
    return scoresdf
