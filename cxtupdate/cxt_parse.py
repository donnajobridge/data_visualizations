import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def clean_cxt_data(cxt, cxt_short):
    cxt_short.rename(columns={'recogcxt':'cxt'}, inplace=True)
    cxt_short = cxt_short[cxt_short['subgroup']=='young']
    cxt_short['cxt'] = cxt_short['cxt'].map({'Cxt1':0, 'Cxt2':1})
    cxt_short.drop('subgroup', axis=1, inplace=True)
    cxt['cxt'] = cxt['cxt'].map({'Cxt A':0, 'Cxt B':1})

    new_cxt = cxt.append(cxt_short)
    new_cxt['exp_screen_size'] = new_cxt.index<800
    new_cxt['exp_screen_size'] = new_cxt['exp_screen_size'].map({True:0, False:1})
    new_cxt['cond']=new_cxt['cond'].map({'active':0, 'passive':1})
    new_cxt = new_cxt[new_cxt['distfix']==1]
    new_cxt = new_cxt[new_cxt['response']>0]
    new_cxt = new_cxt[new_cxt['RT']<20000]
    return new_cxt

def get_response_counts(cxt, act0, act1, pas0, pas1):
    response = cxt.groupby(['sub', 'cond', 'cxt', 'response'])
    response_counts = pd.DataFrame()
    for ind, row in response:
        count = row['response'].count()
        if ind[1] == 0:
            if ind[2] == 0:
                response_counts.loc[ind[0],ind[3]] = count
            else:
                response_counts.loc[ind[0],ind[3]+3] = count
        else:
            if ind[2] == 0:
                response_counts.loc[ind[0],ind[3]+6] = count
            else:
                response_counts.loc[ind[0],ind[3]+9] = count
    response_counts.fillna(value=0, inplace=True)
    old_columns = response.columns.tolist()
    new_columns = act0 + act1 + pas0 + pas1
    response_counts.rename(columns={old_colmns:new_columns}, inplace=True)
    response_counts['act_cxt0_all'] = response_counts[act0].sum(axis=1)
    response_counts['act_cxt1_all'] = response_counts[act1].sum(axis=1)
    response_counts['pas_cxt0_all'] = response_counts[pas0].sum(axis=1)
    response_counts['pas_cxt1_all'] = response_counts[pas1].sum(axis=1)
    return response_counts

def get_prop(condlist, condname, tmp):
    newdf = pd.DataFrame()
    for ind, col in enumerate(condlist):
        newdf[condname +'_'+str(ind+1)] = tmp[col]/tmp[condname +'_all']
    return newdf

def get_prop_tidy(condlist, condname, response_counts):
    newdf = pd.DataFrame()
    props = pd.DataFrame()
    for ind, col in enumerate(condlist):
        newdf['prop'] = tmp[col]/tmp[condname +'_all']
        newdf['locs'] = ind+1
        newdf['cxt'] = condname[-1]
        newdf['cond'] = condname[0:3]
        props=props.append(newdf)
    return props
