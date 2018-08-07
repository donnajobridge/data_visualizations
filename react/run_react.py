import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from react_parse import distance, get_quad, melt_distances
from react_figs import make_layered_hist

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
distance(react, 'x', 'y', 'x3', 'y3', 't3_t1_dist')
distance(react, 'x2', 'y2', 'x3', 'y3', 't3_t2_dist')

#add distance features (from center)
distance(react, 'x', 'y', 'zero', 'zero', 'orig_center_dist')
distance(react, 'x1', 'y1', 'zero', 'zero', 't1_center_dist')
distance(react, 'x2', 'y2', 'zero', 'zero', 't2_center_dist')
distance(react, 'x3', 'y3', 'zero', 'zero', 't3_center_dist')

#get quadrant of each location; add feature
get_quad(react, 'x', 'y', 'loc_quad')
get_quad(react, 'x1', 'y1', 'loc1_quad')
get_quad(react, 'x2', 'y2', 'loc2_quad')
get_quad(react, 'x3', 'y3', 'loc3_quad')

#use lists to make tidy arrays of each distance variable
t2_list = ['t2_orig_dist', 't2_t1_dist']
t3_list = ['t3_orig_dist', 't3_t1_dist', 't3_t2_dist']
orig_list=['t1_orig_dist', 't2_orig_dist', 't3_orig_dist']

update_colors = ['midnightblue', 'royalblue', 'darkturquoise']
forget_colors = ['darkorchid', 'mediumspringgreen', 'midnightblue']

t2 = melt_distances(react, t2_list, 't2')
t3 = melt_distances(react, t3_list, 't3')
orig = melt_distances(react, orig_list, 'orig')


make_layered_hist(react, t2_list, 'Day2')
make_layered_hist(react, t3_list, 'Day3', update_colors)
make_layered_hist(react, orig_list, 'Day3', forget_colors)
