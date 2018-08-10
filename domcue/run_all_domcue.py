from pathlib import *
import numpy as np
import pandas as pd
from behave_parse_domcue import *
from eye_parse_domcue import *


behavestring = '/Volumes/Voss_Lab/EEG/domcueMIXED_djb/behave.data/'
behavepath=Path(behavestring)
eyestring = '/Volumes/Voss_Lab/EEG/domcueMIXED_djb/eye.data/'
eyepath=Path(eyestring)

# run functions
subids = get_subids(behavestring)
for sub in sublist:
    behavepath = set_behavior_path(sub, behavestring)
    behavearray = read_behave_file(behavepath)
    behavearray = apply_adjust_pres_coords(behavearray)


    masterdf = get_eye_files(subids,eyepath)
    eye_sub = masterdf[masterdf['subject']==sub]

    studydf = events_to_df(study)
    studyeyearray = eventsdf_cleanup(studydf)

    restudydf = events_to_df(restudy)
    restudeyearray = eventsdf_cleanup(restudydf)
