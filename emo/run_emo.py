import pandas as pd
from emo_parse import get_emo_scores, get_emo_wide, get_emo_tidy
from emo_figs import emo_confusion, make_bar, make_line

#read in csv
emo=pd.read_csv('emo.csv')
accuracy=emo['response code']==emo['old/new']
emo['accuracy']=accuracy.map({True:1, False:0})
emo['up/in']=emo['up/in'].map({'in':'Inverted', 'up':'Upright'})

## create data frames for plotting
emo_scores=get_emo_scores(emo)
emo_wide=get_emo_wide(emo)
emo_tidy=get_emo_tidy(emo)

emo_confusion(emo)
make_bar(emo_scores)
make_line(emo_scores)
