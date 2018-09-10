from pathlib import *
import numpy as np
import pandas as pd

def get_subs_from_eyebehave(behavestring):
    behavepath=Path(behavestring)
    subfiles="*eyebehave.csv"
    sublist = []
    for filepathobj in behavepath.glob(subfiles):
        fname=filepathobj.name
        sub = fname[:3]
        sublist.append(sub)
    sublist.sort()
    return sublist

def make_timeseries(subcleandf, condnum):
    studytimearray = pd.DataFrame(index=range(4500), columns=range(0,145))
    restudytimearray = pd.DataFrame(index=range(4500), columns=range(0,145))
    fix = subcleandf[(subcleandf['event']=='EFIX') & (subcleandf['cond']==condnum)]
    offmask = (fix['startloc'] == 'offscreen')
    fix.loc[offmask, 'startloc'] = np.nan
    trialcount = 0
    for groups, ldf in fix.groupby(by=['trialnum', 'phase']):
        trial, phase = groups
        for item, trialinfo in ldf.iterrows():
            start = trialinfo['start']
            end = trialinfo['end']
            loc = trialinfo['startloc']
            accuracy = trialinfo['all_accuracy']
            if not accuracy:
                continue
            if phase == 'study':
                studytimearray.iloc[start:end, trial] = loc
            elif phase == 'restudy':
                restudytimearray.iloc[start:end, trial] = loc

    studytimearray.dropna(axis=1, how='all', inplace = True)
    restudytimearray.dropna(axis=1, how='all', inplace = True)
    return studytimearray, restudytimearray


def get_timeseries_props(timearray, sub):
    numtrials = timearray.shape[1]
    props = pd.DataFrame(index=range(timearray.shape[0]))
    alltot = timearray.count(axis=1)
    props['total_fix'] = alltot
    objlist = ['manip_objstart', 'test_objstart', 'other_objstart', 'screen']

    for loc in objlist:
        objset = timearray[timearray==loc].count(axis=1)
        props[loc] = objset/alltot

    props.reset_index(inplace=True)
    props.rename(columns={'index':'time'}, inplace=True)
    props['sub'] = sub
    return props

def get_timeseries_allsubs(subids, behavestring):
    # import each subs data file, run timeseries analysis and then append
    actstudypropAll = pd.DataFrame()
    actrestudypropAll = pd.DataFrame()
    passtudypropAll = pd.DataFrame()
    pasrestudypropAll = pd.DataFrame()
    for sub in subids:
        print('running', sub)
        subfile = behavestring + sub + 'eyebehave.csv'
        subcleandf = pd.read_csv(subfile)
        # remove "catch" trials
        subcleandf = subcleandf[subcleandf['cond']>0]
        subcleandf.reset_index(drop=True, inplace=True)
        actstudytimearray, actrestudytimearray = make_timeseries(subcleandf, 1)
        passtudytimearray, pasrestudytimearray = make_timeseries(subcleandf, 2)

        actstudyprops = get_timeseries_props(actstudytimearray, sub)
        actrestudyprops = get_timeseries_props(actrestudytimearray, sub)

        passtudyprops = get_timeseries_props(passtudytimearray, sub)
        pasrestudyprops = get_timeseries_props(pasrestudytimearray, sub)

        actstudypropAll=pd.concat([actstudypropAll,actstudyprops])
        actrestudypropAll=pd.concat([actrestudypropAll,actrestudyprops])

        passtudypropAll=pd.concat([passtudypropAll,passtudyprops])
        pasrestudypropAll=pd.concat([pasrestudypropAll,pasrestudyprops])

    return actstudypropAll, actrestudypropAll, passtudypropAll, pasrestudypropAll

def downsample_timeseries(timearray, newsamplerate):
    alltimes = timearray.time.unique()
    times_to_keep = alltimes[0:len(alltimes):newsamplerate]
    downsampled = timearray.set_index('time')
    downsampled = downsampled.loc[times_to_keep,:]
    return downsampled
