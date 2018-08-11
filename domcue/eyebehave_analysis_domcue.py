import numpy as np
import pandas as pd


def make_timeseries(subcleandf, condnum):
    studytimearray = pd.DataFrame(index=range(4500), columns=range(0,161))
    restudytimearray = pd.DataFrame(index=range(4500), columns=range(0,161))
    fix = subcleandf[(subcleandf['event']=='EFIX') & (subcleandf['cond']==condnum)]
    trialcount = 0
    for groups, ldf in fix.groupby(by=['trialnum', 'phase']):
        trial, phase = groups
        for item, trialinfo in ldf.iterrows():
            start = trialinfo['start']
            end = trialinfo['end']
            loc = trialinfo['startloc']
            if phase == 'study':
                studytimearray.iloc[start:end, trial] = loc
            elif phase == 'restudy':
                restudytimearray.iloc[start:end, trial] = loc
    studytimearray.dropna(axis=1, how='all', inplace = True)
    restudytimearray.dropna(axis=1, how='all', inplace = True)
    return studytimearray, restudytimearray

def get_timeseries_props(timearray):
    numtrials = timearray.shape[1]
    props = pd.DataFrame(index=range(timearray.shape[0]))

    alltot = timearray.count(axis=1)
    props['total_fix'] = alltot

    objlist = ['obj1start', 'obj2start', 'obj3start', 'screen', 'offscreen']

    for loc in objlist:
        objset = timearray[timearray==loc].count(axis=1)
        props[loc] = objset/numtrials
    return props
    
