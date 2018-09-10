from pathlib import *
import numpy as np
import pandas as pd
from behave_parse import *
from eye_parse import *
from eye_behave_converge import *

behavestring = '/Volumes/Voss_Lab/MRI/domchoicefmri_djb/behave.data/'
behavepath=Path(behavestring)
eyestring = '/Volumes/Voss_Lab/MRI/domchoicefmri_djb/eye.data/'
eyepath=Path(eyestring)

# run functions
subids = get_subids(behavepath)

for sub in subids:
    if sub == '918':
        continue
    if int(sub) < 900:
        xmax = 1920/2
        ymax = 1080/2
    else:
        xmax = 1280/2
        ymax = 1024/2

    # process behavior
    studyfilepath = set_behavior_path(sub, behavestring, 'study')
    studyarray = read_study_file(studyfilepath)

    testfilepath = set_behavior_path(sub, behavestring, 'test')
    testarray = read_test_file(testfilepath)
    # merge study & test
    behavearray = merge_study_test(studyarray, testarray)
 # adjust coords
    behavearray = apply_adjust_pres_coords(behavearray,sub,xmax,ymax)
# define manipulated object, tested object, and other object from obj1, obj2, obj3
    alldomarray, alltestarray, allotherarray = define_obj_types(behavearray)
# add in new object identities and remove old ones
    print(sub)
    print(behavearray.shape)
    print(alldomarray.shape)
    print(alltestarray.shape)
    print(allotherarray.shape)
    behavearray = edit_obj_ids(behavearray, alldomarray, alltestarray, allotherarray)

    # get eye files and process
    masterdf = get_eye_files(subids,eyepath)
    eye_sub = masterdf[masterdf['subject']==sub]
    study, restudy = parse_eye_line(eye_sub, eyestring)

    studydf = events_to_df(study)
    studyeyearray = eventsdf_cleanup(studydf)
    restudydf = events_to_df(restudy)
    restudeyearray = eventsdf_cleanup(restudydf)
    # concatenate study and restudy eye arrays
    studyeyearray['phase']='study'
    restudeyearray['phase']='restudy'
    eyearray = pd.concat([studyeyearray, restudeyearray], ignore_index=True)

    # combine behavior & eye data
    eyebehave = eye_behave_combo(eyearray, behavearray)

    # calculate distances for start and end eye locations
    startdistarray=calculate_dist(eyebehave,x1='xstart',y1='ystart',name='start')
    enddistarray=calculate_dist(eyebehave,'xend','yend','end')

    # start & end locations
    eyebehave=loc_view(eyebehave,startdistarray,'startloc')
    eyebehave=loc_view(eyebehave,enddistarray,'endloc')

    #append start & end distances to eyebehave array
    eyebehave=pd.concat([eyebehave, startdistarray, enddistarray], axis=1)

    ''' change df to dict'''
    eyebehavedict=eyebehave.to_dict('records')
    ''' determine if non-loc viewing was on screen or offscreen'''
    eyebehavedict=assign_screenview(eyebehavedict,'xstart','ystart','start',xmax, ymax)
    eyebehavedict=assign_screenview(eyebehavedict,'xend','yend','end',xmax, ymax)

    '''adjust artifacts in eye data due to blinks'''
    new_previous_events=adjust_fix_before_blink(eyebehavedict)
    corrected_eye_events=adjust_event_after_blink(new_previous_events)

    '''put data back in df and remove old blinks'''
    subcleandf=eyedict_backto_df(corrected_eye_events)
    subcleandf['sub'] = sub

    fname='data/'+sub+'eyebehave.csv'
    subcleandf.to_csv(fname)
    print(sub, 'is done!')
