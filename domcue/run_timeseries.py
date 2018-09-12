import pandas as pd
import numpy as np


# read in all sub files

# make regular spaced timeseries
actstudytimearray, actrestudytimearray = make_timeseries(subcleandf, 1)
passtudytimearray, pasrestudytimearray = make_timeseries(subcleandf, 2)

# get prop viewing time for timeseries

actstudyprops = get_timeseries_props(actstudytimearray)
actrestudyprops = get_timeseries_props(actrestudytimearray)

passtudyprops = get_timeseries_props(passtudytimearray)
pasrestudyprops = get_timeseries_props(pasrestudytimearray)
