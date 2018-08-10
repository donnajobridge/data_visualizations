from pathlib import *
import numpy as np
import pandas as pd


def get_subids(behavestring):
    subfiles="*study"
    sublist = []
    for filepathobj in behavepath.glob(subfiles):
        fname=filepathobj.name
        sub = fname[:3]
        sublist.append(sub)
    sublist.sort()
    return sublist

def set_behavior_path(sub, behavestring):
    extra='study'
    behaveobj=[behavestring+sub+extra]
    behavepath=Path(behaveobj[0])
    behavepath.exists()
    return behavepath

def read_behave_file(filepath):
    """read in behavearray, turn into DataFrame and delete extra columns"""
    colnames=['obj1','obj2','obj3','cuecond','loc1','x1','y1','loc2','x2','y2','loc3','x3','y3',
     'domRT','dom_resp','cond','block','tmp', 'tmp']
    behavearray=pd.read_table(filepath,header=None,names=colnames)
    tmpmask=~behavearray.columns.str.contains('tmp')
    behavearray=behavearray[behavearray.columns[tmpmask]]
    trialnum = np.arange(1,len(behavearray)+1)
    behavearray['studytrial'] = trialnum
    return behavearray

def adjust_pres_coords(array,x,y,xmax=1920/2,ymax=1080/2):
    """adjustment for behavioral coords to match
    eye coords for presentation version of exp"""
    newarray=pd.DataFrame()
    newarray[x]=array[x]+xmax
    newarray[y]=(array[y]-ymax)*-1
    return newarray

def apply_adjust_pres_coords(behavearray):
    """applies adjust_pres_coords to all
    coords in behave array"""
    xs = [f'x{loc}' for loc in range(1,4)]
    ys = [f'y{loc}' for loc in range(1,4)]
    newlocs = pd.DataFrame()
    for loc in zip(xs, ys):
        x = loc[0]
        y = loc[1]
        newloc=adjust_pres_coords(behavearray, x, y)
        newlocs[x] = newloc[x]
        newlocs[y] = newloc[y]

    cols=newlocs.columns.tolist()
    for loc in cols:
        behavearray[loc]=newlocs[loc]
    return behavearray
