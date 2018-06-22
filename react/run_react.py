import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from react_parse import distance


#read in react file and make adjustments
react=pd.read_table('data/react_raw.csv', index_col=False)
react=react[react['cond']==1]
react.drop('cond', axis=1, inplace=True)
react['zero']=0

#add distance features (between locs)
distance(react, 'x', 'y', 'x1', 'y1', 't1_orig_dist')
distance(react, 'x', 'y', 'x2', 'y2', 't2_orig_dist')
distance(react, 'x1', 'y1', 'x2', 'y2', 't2_t1_dist')
distance(react, 'x', 'y', 'x3', 'y3', 't3_orig_dist')
distance(react, 'x2', 'y2', 'x3', 'y3', 't3_t2_dist')

#add distance features (from center)
distance(react, 'x', 'y', 'zero', 'zero', 'orig_center_dist')
distance(react, 'x1', 'y1', 'zero', 'zero', 't1_center_dist')
distance(react, 'x2', 'y2', 'zero', 'zero', 't2_center_dist')
distance(react, 'x3', 'y3', 'zero', 'zero', 't3_center_dist')
