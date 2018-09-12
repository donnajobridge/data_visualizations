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
    actstudypropAll.to_csv('data/actstudyprop_allaccdom.csv')
    actrestudypropAll.to_csv('data/actrestudyprop_allaccdom.csv')
    passtudypropAll.to_csv('data/passtudyprop_allaccdom.csv')
    pasrestudypropAll.to_csv('data/pasrestudyprop_allaccdom.csv')
else:
    # just load the existing data:
    actstudypropAll = pd.read_csv('data/actstudyprop_allacc.csv')
    actrestudypropAll = pd.read_csv('data/actrestudyprop_allacc.csv')
    passtudypropAll = pd.read_csv('data/passtudyprop_allacc.csv')
    pasrestudypropAll = pd.read_csv('data/pasrestudyprop_allacc.csv')

    actstudypropAll = actstudypropAll[actstudypropAll['sub']>899]
    actrestudypropAll = actrestudypropAll[actrestudypropAll['sub']>899]
    passtudypropAll = passtudypropAll[passtudypropAll['sub']>899]
    pasrestudypropAll = pasrestudypropAll[pasrestudypropAll['sub']>899]


actstudyprop = downsample_timeseries(actstudypropAll, 100)
actrestudyprop = downsample_timeseries(actrestudypropAll, 100)
passtudyprop = downsample_timeseries(passtudypropAll, 100)
pasrestudyprop = downsample_timeseries(pasrestudypropAll, 100)

allarrays = [actstudyprop, actrestudyprop, passtudyprop, pasrestudyprop]

for array in allarrays:
    array['nondom'] = array['test_objstart'] + array['other_objstart']

objlist = ['manip_objstart', 'test_objstart', 'other_objstart', 'screen', 'nondom']


colorlist = ['midnightblue', 'darkturquoise']
restudylist = [actrestudyprop, pasrestudyprop]
condlist = ['Active', 'Passive']

make_layered_lineplot(restudylist, condlist, 'manip_objstart', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'nondom', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'other_objstart', colorlist, 'restudy')
make_layered_lineplot(restudylist, condlist, 'test_objstart', colorlist, 'restudy')
