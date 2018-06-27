import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
<<<<<<< HEAD
from cxt_parse import clean_cxt_data, get_response_counts, get_prop
from cxt_figs import get_cxt_figs

cxt = pd.read_csv('data/cxtupdatearrayfmri.csv', index_col=[0],
usecols=['sub', 'cond', 'cxt', 'block', 'response', 'RT', 'updatedistraw', 'luredistfix', 'distfix'])

cxt_short = pd.read_csv('data/cxtupdateEPIyoungold.csv', index_col=[0],
usecols=['sub', 'cond', 'recogcxt', 'subgroup', 'block', 'response', 'RT',
'updatedistraw', 'luredistfix', 'distfix'])

cxt = clean_cxt_data(cxt, cxt_short)
response_counts = get_response_counts(cxt)

props_wide, props_tidy = get_prop(response_counts)

get_cxt_figs(props_tidy)
