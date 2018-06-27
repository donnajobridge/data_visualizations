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


<<<<<<< HEAD
def melt_distances(means, condlist, day):
=======
def melt_distances(array, condlist, day):
    means=pd.DataFrame(array.groupby(['sub'])[condlist].mean())
    means.reset_index(inplace=True)
>>>>>>> 3d4fa542af18c1eb83ac59f51122de37b4a45030
    tidy_dists=means.melt(id_vars=['sub'], value_vars=condlist,
              var_name=day +'_measure', value_name=day+'_dist')
    return tidy_dists
