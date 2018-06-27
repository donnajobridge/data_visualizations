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
    print('shape of new_cxt=',new_cxt.shape)
    return new_cxt

def get_response_counts(new_cxt):
    response = new_cxt.groupby(['sub', 'cond', 'cxt', 'response'])
    response_counts = pd.DataFrame()
    for ind, row in response:
        sub, cond, cxt, response = ind
        count=row['response'].count()
        cond_map = {0:'act', 1:'pas'}
        cond_name = cond_map[cond]
        colname = f'{cond_name}_cxt{cxt}_loc{response}'
        response_counts.loc[sub,colname]=count
    response_counts.fillna(value=0, inplace=True)
    for cond in ['act', 'pas']:
        for cxt in [0,1]:
            new_col=f'{cond}_cxt{cxt}_all'
            col_list= [f'{cond}_cxt{cxt}_loc{loc}' for loc in range(1,4)]
            response_counts[new_col] = response_counts[col_list].sum(axis=1)
    return response_counts

def get_prop(condlist, condname, response_counts):
    newdf = pd.DataFrame()
    for ind, col in enumerate(condlist):
        newdf[condname +'_'+str(ind+1)] = response_counts[col]/response_counts[condname +'_all']
    return newdf

def get_prop_tidy(condlist, condname, response_counts):
    newdf = pd.DataFrame()
    props = pd.DataFrame()
    for ind, col in enumerate(condlist):
        newdf['prop'] = response_counts[col]/response_counts[condname +'_all']
        newdf['locs'] = ind+1
        newdf['cxt'] = condname[-1]
        newdf['cond'] = condname[0:3]
        props=props.append(newdf)
    return props
