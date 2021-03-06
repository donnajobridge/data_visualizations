from pathlib import *
import numpy as np
import pandas as pd

def eye_behave_combo(eyearray,behavearray):
    eyebehave=eyearray.copy()
    eyecols=eyebehave.columns.tolist()
    behavecols=['manip_x','manip_y','test_x','test_y','other_x','other_y','cond', 'manip_accuracy', 'studytrial', 'testtrial',
                'recog_accuracy', 'recog_loc_accuracy', 'manip_accuracy', 'cuecond']
    allcols=eyecols+behavecols
    eyebehave=eyebehave.reindex(columns=allcols)
    order_col='studytrial'
    behavearray.sort_values(by=[order_col], inplace=True)
    behavearray.set_index(order_col, drop=False, inplace=True)
    for trial in range(0,behavearray.shape[0]):
        eyetrialevents=(eyebehave['trialnum']==trial+1)
        eyetrial=eyebehave.loc[eyetrialevents]
        for col in behavecols:
            eyetrial.loc[eyetrialevents,col]=behavearray.loc[trial+1,col]

        eyebehave.loc[eyetrialevents]=eyetrial
    return eyebehave


def dist(array,x1,y1,x2,y2):
    """ distance formula for columns of coords"""
    dx=array[x1]-array[x2]
    dy=array[y1]-array[y2]
    dist=np.sqrt(dx**2+dy**2)
    return dist

def calculate_dist(eyebehave,x1,y1,name):
    """ calculate distances for start and end eye locations"""
    for x in eyebehave:
        distdict={'manip_obj':dist(eyebehave,x1,y1,'manip_x','manip_y'),
                        'test_obj':dist(eyebehave,x1,y1,'test_x','test_y'),
                        'other_obj':dist(eyebehave,x1,y1,'other_x','other_y')}

    distarray=pd.DataFrame(distdict)
    col=distarray.columns.tolist()
    distarray.columns=[c+name for c in col]
    return distarray


def loc_view(eyebehave,distarray,name):
    distarray.idxmin(axis=1)
    mindistmask=distarray.min(axis=1)<180
    distmins=distarray.loc[mindistmask]

    distminlocs=distmins.idxmin(axis=1)
    eyebehave[name]="none"
    eyebehave.loc[mindistmask,name]=distminlocs
    return eyebehave

def screenview(x,y,xmax,ymax):
    screen='screen'
    if x>xmax:
        screen='offscreen'
    if x<(0):
        screen='offscreen'
    if y>ymax:
        screen='offscreen'
    if y<(0):
        screen='offscreen'
    return screen

def assign_screenview(eyebehavedict,xname,yname,name,xmax,ymax):
    colname=name+'loc'
    for loc in eyebehavedict:
        screen=screenview(loc[xname],loc[yname],xmax,ymax)
        if loc[colname]=='none':
            loc[colname]=screen
        if name !='end':
            continue
        if loc['event']=='EFIX':
            loc[colname]=np.nan
    return eyebehavedict


def adjust_fix_before_blink(eyebehavedict):
    """replace fixations <100 ms before blinks"""
    tmp_dict=eyebehavedict.copy()
    new_previous_events=[]
    for i,ind in enumerate(tmp_dict):
        current_event = ind
        if i>0:
            if current_event['event']=='EBLINK':
                if previous_event['trialnum']==current_event['trialnum']:
                    if previous_event['event']=='EFIX' and previous_event['duration']<100:
                        previous_event['event']='blink'
            new_previous_events.append(previous_event)
        previous_event=ind
    new_previous_events.append(previous_event)
    return new_previous_events

def adjust_event_after_blink(new_previous_events):
    new_post_events=[]
    new_events=new_previous_events.copy()
    flag=False
    for current_event in new_events:
        event_type=current_event['event']
        current_trial=current_event['trialnum']
        if flag==True and previous_trial==current_trial:
            if event_type=='ESACC':
                event_type='blink'
            elif event_type=='EFIX':
                if current_event['duration']<100:
                    event_type='blink'
        new_post_events.append(current_event)
        flag=(event_type=='EBLINK')
        previous_trial=current_trial
    return new_post_events

def eyedict_backto_df(new_post_events):
    corrected_eyedf=pd.DataFrame(new_post_events)
    old_blink_mask=corrected_eyedf['event']!='EBLINK'
    corrected_eyedf=corrected_eyedf[old_blink_mask]
    corrected_eyedf.sort_values(['block','trialnum','start'])
    corrected_eyedf=corrected_eyedf.reset_index(drop=True)
    corrected_eyedf['cuecond']=corrected_eyedf['cuecond'].map({1:1, 2:0})
    corrected_eyedf['recog+manip_accuracy'] = ((corrected_eyedf['manip_accuracy']) &
                              (corrected_eyedf['recog_accuracy']))
    corrected_eyedf['recog+manip+loc_accuracy'] = ((corrected_eyedf['manip_accuracy']) &
                              (corrected_eyedf['recog_accuracy']) & (corrected_eyedf['recog_loc_accuracy']))
    corrected_eyedf['dom_all_accuracy'] = ((corrected_eyedf['recog+manip+loc_accuracy']) & (corrected_eyedf['cuecond']))

    return corrected_eyedf
