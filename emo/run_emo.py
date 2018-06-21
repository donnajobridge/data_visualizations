import pandas as pd
from emo_parse import get_emo_scores, get_emo_wide, get_emo_tidy
from emo_figs import emo_confusion, make_bar

#read in csv
emo=pd.read_csv('emo.csv')
accuracy=emo['response code']==emo['old/new']
emo['accuracy']=accuracy.map({True:1, False:0})

## create data frames for plotting
emo_scores=get_emo_scores(emo)
emo_wide=get_emo_wide(emo)
emo_tidy=get_emo_tidy(emo)

emo_confusion(emo, 's')
emo_confusion(emo, 'h')

make_bar(emo_scores, 'f1')
make_bar(emo_scores, 'recall')
make_bar(emo_scores, 'precision')
