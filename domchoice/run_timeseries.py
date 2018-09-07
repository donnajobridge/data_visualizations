from pathlib import *
import numpy as np
import pandas as pd
from make_timeseries import *
from make_timeseries_figs import *

behavestring = 'data/'

subids = get_subs_from_eyebehave(behavestring)

makefiles = 1

if makefiles ==0:
    # create prop timeseries for all subs & save master arrays
    actstudypropAll, actrestudypropAll, passtudypropAll, pasrestudypropAll = get_timeseries_allsubs(subids, behavestring)
    actstudypropAll.to_csv('data/actstudyprop_dom.csv')
    actrestudypropAll.to_csv('data/actrestudyprop_dom.csv')
    passtudypropAll.to_csv('data/passtudyprop_dom.csv')
    pasrestudypropAll.to_csv('data/pasrestudyprop_dom.csv')
else:
    # just load the existing data:
    actstudypropAll = pd.read_csv('data/actstudyprop_dom.csv')
    actrestudypropAll = pd.read_csv('data/actrestudyprop_dom.csv')
    passtudypropAll = pd.read_csv('data/passtudyprop_dom.csv')
    pasrestudypropAll = pd.read_csv('data/pasrestudyprop_dom.csv')


actstudyprop = downsample_timeseries(actstudypropAll, 100)
actrestudyprop = downsample_timeseries(actrestudypropAll, 100)
passtudyprop = downsample_timeseries(passtudypropAll, 100)
pasrestudyprop = downsample_timeseries(pasrestudypropAll, 100)

allarrays = [actstudyprop, actrestudyprop, passtudyprop, pasrestudyprop]

for array in allarrays:
    array['nondom'] = array['obj2start'] + array['obj3start']

objlist = ['obj1start', 'obj2start', 'obj3start', 'screen', 'nondom']


colorlist = ['midnightblue', 'darkturquoise']
restudylist = [actrestudyprop, pasrestudyprop]
condlist = ['Active', 'Passive']

make_layered_lineplot(restudylist, condlist, 'obj1start', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'nondom', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'screen', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'obj3start', colorlist, 'restudy')
