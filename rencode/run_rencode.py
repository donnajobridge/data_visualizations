import pandas as pd
from rencode_parse import get_props_tidy_all, get_props_tidy_highconf, get_dprime, get_score_data
from rencode_figs import make_rencode_figs, make_cm_matrix
from scipy.stats import norm

Z = norm.ppf

# read in data file
rencode=pd.read_csv('data/rencode_cxtlocBEHAVEeeg.csv', header=0, usecols=['sub', 'cond', 'cxtcond', 'old/new', 'recog_answer', 'refresh_medsplit',
       'recog confidence', 'refresh dist', 'loc1_x', 'loc1_y', 'loc2_x', 'loc2_y', 'refreshRT', 'refresh_order',
       'block', 'old/newRT', 'confidence RT'])

# calculate accuracy column
rencode['old/new']=rencode['old/new'].map({'old':0, 'new':1})
rencode['recog_answer']=rencode['recog_answer'].map({'old resp':0, 'new resp':1})
rencode['accuracy']=rencode['old/new']==rencode['recog_answer']
rencode['accuracy']=rencode['accuracy'].map({False:0, True:1})

propsdf = get_props_tidy_all(rencode)
propsdf_high = get_props_tidy_highconf(rencode)

dprime_all = get_dprime(propsdf, Z)
dprime_high = get_dprime(propsdf_high, Z)

scoresdf = get_score_data(rencode)

mem = ['dprime', 'hit', 'fa']
datascience = ['recall', 'precision', 'f1']

make_rencode_figs(dprime_all, mem, 'all')
make_rencode_figs(dprime_high, mem, 'high')
make_rencode_figs(scoresdf, datascience, 'all')
make_cm_matrix(rencode)
