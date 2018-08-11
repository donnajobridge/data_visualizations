from pathlib import *
import numpy as np
import pandas as pd


def parse_eye_filename(pathobject):
    fname=pathobject.name
    parts=fname.split(".")[0]
    subject=parts[:3]
    block=parts[3:4]
    subdict={"subject":subject, "block":block, "fname":fname}
    return subdict

def get_eye_files(subids,eyepath):
    """ returns master dataframe including eye file name, block, phase, subid
    input list of subject strings, Path object pointing to eye files
    """
    substrings=[s+"*.asc" for s in subids]
    subinfo=[]
    for s in substrings:
        for filepathobj in eyepath.glob(s):
            subdict=parse_eye_filename(filepathobj)
            subinfo.append(subdict)

    masterdf=pd.DataFrame(subinfo).sort_values(by=["subject","block"])
    print(masterdf.head())
    masterdf=masterdf[["subject","block","fname"]]
    masterdf.index=range(len(masterdf))
    return masterdf

def parse_eye_events_to_intline(line,extrainfo):
    efixspace=["","",""]
    eblinkspace=efixspace*2
    newline=line.split()
    if "EFIX" in line:
        newline.extend(efixspace)
    elif "EBLINK" in line:
        newline.extend(eblinkspace)
    newline.extend(extrainfo)
    return newline

def parse_eye_line(eye_sub, eyestring):
    """ parses each line of eye file for a given eye_phase_sub
    input one phase type list of files for a subs
    and the path to the file (in form of a string)
    outputs dataframe with all events in table
    """
    etypes=('ESACC','EFIX','EBLINK')
    study=[]
    restudy=[]
    blocks=eye_sub.block
    fnames=eye_sub.fname
    subjects=eye_sub.subject
    totalcount=0
    trialnum=0
    print(eyestring)
    for block,fname,subject in zip(blocks,fnames,subjects):
        path_file=eyestring+fname
        startcount=0
        p=Path(path_file)
        with p.open() as f:
            for line in f:
                if "START" in line:
                    totalcount=totalcount+1
                    startline=line.split()
                    starttime=int(startline[1])
                    if totalcount % 2:
                        trialnum = trialnum+1

                if any(e in line for e in etypes):
                    extrainfo=[starttime,trialnum,block,subject]
                    newline=parse_eye_events_to_intline(line,extrainfo)
                    if totalcount % 2:
                        study.append(newline)
                    else:
                        restudy.append(newline)
            print(trialnum, block, startcount)
    return study, restudy


def events_to_df(events):
    """ change raw events to data DataFrame
    then and change values to numeric"""

    eye_events_df=pd.DataFrame(events)
    eye_events_df=eye_events_df.apply(pd.to_numeric,errors='ignore')
    headers=["event","eye","start","end","duration",
    "xstart","ystart","xend","yend","?","?","trialstart",
    "trialnum","block","sub"]
    eye_events_df.columns=headers
    return eye_events_df

def eventsdf_cleanup(eye_events_df):
    x=pd.DataFrame()
    """adjust trial start time, remove irrelevant values in fixation rows,
    and then delete excess columns"""

    eyedf_clean=eye_events_df.copy()

    eyedf_clean['start']=eyedf_clean['start']-eyedf_clean['trialstart']
    eyedf_clean['end']=eyedf_clean['end']-eyedf_clean['trialstart']

    efix_mask = (eyedf_clean["event"]=="EFIX")
    eyedf_clean.loc[efix_mask, 'xend'] = np.nan
    for col in ['xstart', 'ystart', 'xend', 'yend']:
        x = eyedf_clean[col]
        eyedf_clean[col] = pd.to_numeric(x, errors='coerce')


    del eyedf_clean['trialstart']
    del eyedf_clean['?']
    del eyedf_clean['eye']

    return eyedf_clean
