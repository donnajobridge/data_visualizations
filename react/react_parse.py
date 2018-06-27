import pandas as pd
import numpy as np



def distance(array, x1, y1, x2, y2, new_col):
    dx=array[x2]-array[x1]
    dy=array[y2]-array[y1]
    array[new_col]=np.sqrt(dx**2+dy**2)
    return array

def get_quad(array, x, y, new_col):
    for sub, row in array.iterrows():
        if (array.loc[sub, x]<0) & (array.loc[sub, y]<0):
                array.loc[sub, new_col]=3
        elif (array.loc[sub, x]<0) & (array.loc[sub, y]>0):
                array.loc[sub, new_col]=2
        elif (array.loc[sub, x]>0) & (array.loc[sub, y]<0):
                array.loc[sub, new_col]=4
        elif (array.loc[sub, x]>0) & (array.loc[sub, y]>0):
                array.loc[sub, new_col]=1
        else: array.loc[sub, new_col]=np.nan
    return array


def melt_distances(means, condlist, day):
    tidy_dists=means.melt(id_vars=['sub'], value_vars=condlist,
              var_name=day +'_measure', value_name=day+'_dist')
    return tidy_dists
