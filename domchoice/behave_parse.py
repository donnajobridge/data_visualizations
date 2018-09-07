from pathlib import *
import numpy as np
import pandas as pd

def get_subids(behavepath):
    subfiles="*study"
    sublist = []
    for filepathobj in behavepath.glob(subfiles):
        fname=filepathobj.name
        sub = fname[:3]
        sublist.append(sub)
    sublist.sort()
    return sublist

def set_behavior_path(sub, behavestring, extra):
    behaveobj=[behavestring+sub+extra]
    behavefilepath=Path(behaveobj[0])
    behavefilepath.exists()
    return behavefilepath

def read_study_file(filepath):
    """read in studyarray, turn into DataFrame and delete extra columns"""
    colnames=['obj1','obj2','obj3','cuecond','loc1','x1','y1','loc2','x2','y2','loc3','x3','y3',
     'dom_loc_rt','dom_loc_resp','cond','block','obj_type', 'dom_obj_id', 'dom_loc_actual', 'dom_choice_rt']
    studyarray=pd.read_table(filepath,header=None,names=colnames)
    tmpmask=~studyarray.columns.str.contains('tmp')
    studyarray=studyarray[studyarray.columns[tmpmask]]
    trialnum = np.arange(1,len(studyarray)+1)
    studyarray['studytrial'] = trialnum
    return studyarray

def read_test_file(filepath):
    """read in testarray, turn into DataFrame and delete extra columns"""
    colnames=['obj1','obj2','obj3','cuecond','loc1','x1','y1','loc2','x2','y2','loc3','x3','y3',
     'dom_loc_rt','dom_loc_resp','cond','block','obj_type', 'dom_obj_id', 'dom_loc_actual', 'dom_choice_rt',
             'tmp', 'tmp', 'test_obj_id', 'test_loc_id', 'tmp', 'tmp', 'tmp', 'tmp', 'test_resp', 'test_obj_rt',
             'test_loc_id', 'test_loc_rt', 'conf', 'tmp']
    testarray=pd.read_table(filepath,header=None,names=colnames)
    tmpmask=~testarray.columns.str.contains('tmp')
    testarray=testarray[testarray.columns[tmpmask]]
    trialnum = np.arange(1,len(testarray)+1)
    testarray['testtrial'] = trialnum
    testarray['recog_accuracy'] = testarray['test_resp'] == 1
    testarray['recog_loc_accuracy'] = (testarray['test_loc_id'] == testarray['loc1']) | (testarray['test_loc_id'] == testarray['loc2']) | (testarray['test_loc_id'] == testarray['loc3'])
    testarray['dom_accuracy'] = testarray['dom_loc_resp'] == testarray['dom_loc_actual']
    return testarray

# merge study & test
def merge_study_test(studyarray, testarray):
    # merge study & test
    testarray['obj1'] = testarray['obj1'] + (1000*testarray['obj_type'])
    testarray = testarray.set_index('obj1')
    studyarray['obj1'] = studyarray['obj1'] + (1000*studyarray['obj_type'])
    studyarray.sort_values('obj1')
    studyarray = studyarray.set_index('obj1')
    behavearray = studyarray.copy()

    for ind, ldf in testarray.iterrows():
        for col in ['dom_accuracy', 'recog_accuracy', 'recog_loc_accuracy', 'testtrial']:
            behavearray.loc[ind, col] = ldf[col]
    behavearray.reset_index(inplace=True)
    return behavearray

def adjust_pres_coords(array,x,y,xmax,ymax):
    """adjustment for behavioral coords to match
    eye coords for presentation version of exp"""
    newarray=pd.DataFrame()
    newarray[x]=array[x]+xmax
    newarray[y]=(array[y]-ymax)*-1
    return newarray

def apply_adjust_pres_coords(behavearray, sub, xmax,ymax):
    """applies adjust_pres_coords to all
    coords in behave array"""


    xs = [f'x{loc}' for loc in range(1,4)]
    ys = [f'y{loc}' for loc in range(1,4)]
    newlocs = pd.DataFrame()
    for loc in zip(xs, ys):
        x = loc[0]
        y = loc[1]
        newloc=adjust_pres_coords(behavearray,x,y,xmax,ymax)
        newlocs[x] = newloc[x]
        newlocs[y] = newloc[y]

    cols=newlocs.columns.tolist()
    for loc in cols:
        behavearray[loc]=newlocs[loc]
    return behavearray
