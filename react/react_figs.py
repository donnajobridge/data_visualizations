import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.patches import Rectangle
import seaborn as sns

color=iter(cm.rainbow(np.linspace(0,1,2)))

for dist in t2_list:
   co=next(color)
hist_kde=[sns.distplot(react[dist], color=c, norm_hist=True,
            axlabel='Distance Error (pixels)', hist_kws={'alpha':.5}) for c in t2_list]
handles = [Rectangle((0,0),1,1,color=c,edgecolor="k", alpha=.75) for c in t2_list]
labels= ["Updated", "Original",]
plt.legend(handles, labels)
hist_kde=hist_kde.get_figure()
hist_kde.savefig('react_hist_kde.png')
