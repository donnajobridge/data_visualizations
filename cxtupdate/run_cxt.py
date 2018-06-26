import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cxt_parse import clean_cxt_data, get_response_counts, get_prop, get_prop_tidy


cxt = pd.read_csv('data/cxtupdatearrayfmri.csv', index_col=[0],
usecols=['sub', 'cond', 'cxt', 'block', 'response', 'RT', 'updatedistraw', 'luredistfix', 'distfix'])

cxt_short = pd.read_csv('data/cxtupdateEPIyoungold.csv', index_col=[0],
usecols=['sub', 'cond', 'recogcxt', 'subgroup', 'block', 'response', 'RT',
'updatedistraw', 'luredistfix', 'distfix'])

cxt = clean_cxt_data(cxt, cxt_short)

#define conditions for columns
act0 = ['act_cxt0_loc1', 'act_cxt0_loc2', 'act_cxt0_loc3']
act1 = ['act_cxt1_loc1', 'act_cxt1_loc2', 'act_cxt1_loc3']
pas0 = ['pas_cxt0_loc1', 'pas_cxt0_loc2', 'pas_cxt0_loc3']
pas1 = ['pas_cxt1_loc1', 'pas_cxt1_loc2', 'pas_cxt1_loc3']

response_counts = get_response_counts(cxt, act0, act1, pas0, pas1)

# calculate proportion of responses
act0_prop=get_prop(act0, 'act_cxt0', response_counts)
act1_prop=get_prop(act1, 'act_cxt1', response_counts)
pas0_prop=get_prop(pas0, 'pas_cxt0', response_counts)
pas1_prop=get_prop(pas1, 'pas_cxt1', response_counts)

#make proportions in wide format
props_wide=pd.concat([act0_prop, act1_prop, pas0_prop, pas1_prop], axis=1)

#get props in tidy format
act0_prop=get_prop_tidy(act0, 'act_cxt0', response_counts)
act1_prop=get_prop_tidy(act1, 'act_cxt1', response_counts)
pas0_prop=get_prop_tidy(pas0, 'pas_cxt0', response_counts)
pas1_prop=get_prop_tidy(pas1, 'pas_cxt1', response_counts)

props_tidy=act0_prop.append([act1_prop, pas0_prop, pas1_prop])
