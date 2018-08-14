import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import *
from eyebehave_analysis_domcue import *
from make_domcue_figs import *

behavestring = 'data/'
makefiles = 0
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

subids = get_subs_from_eyebehave(behavestring)

if makefiles ==1:
# get prop timeseries for all subs & save master arrays
    actstudypropAll, actrestudypropAll, passtudypropAll, pasrestudypropAll = get_timeseries_allsubs(subids)
    actstudypropAll.to_csv('data/actstudypropAll.csv')
    actrestudypropAll.to_csv('data/actrestudypropAll.csv')
    passtudypropAll.to_csv('data/passtudypropAll.csv')
    pasrestudypropAll.to_csv('data/pasrestudypropAll.csv')
else:
    # just load the existing data:
    actstudypropAll = pd.read_csv('data/actstudypropAll.csv')
    actrestudypropAll = pd.read_csv('data/actrestudypropAll.csv')
    passtudypropAll = pd.read_csv('data/passtudypropAll.csv')
    pasrestudypropAll = pd.read_csv('data/pasrestudypropAll.csv')

actstudyprop = downsample_timeseries(actstudypropAll, 100)
actrestudyprop = downsample_timeseries(actrestudypropAll, 100)
passtudyprop = downsample_timeseries(passtudypropAll, 100)
pasrestudyprop = downsample_timeseries(pasrestudypropAll, 100)

allarrays = [actstudyprop, actrestudyprop, passtudyprop, pasrestudyprop]

for array in allarrays:
    array['nondom'] = array['obj2start'] + array['obj3start']

objlist = ['obj1start', 'obj2start', 'obj3start', 'screen', 'nondom']

actdiff = actrestudyprop[objlist] - actstudyprop[objlist]
actdiff['sub'] = actrestudyprop['sub']
pasdiff = pasrestudyprop[objlist] - passtudyprop[objlist]
pasdiff['sub'] = pasrestudyprop['sub']


colorlist = ['midnightblue', 'darkturquoise']
restudylist = [actrestudyprop, pasrestudyprop]
difflist = [actdiff, pasdiff]
condlist = ['Active', 'Passive']

make_layered_lineplot(restudylist, condlist, 'obj1start', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'nondom', colorlist, 'restudy')

make_layered_lineplot(difflist, condlist, 'obj1start', colorlist, 'diff')
make_layered_lineplot(difflist, condlist, 'nondom', colorlist, 'diff')
