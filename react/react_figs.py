import matplotlib.pyplot as plt
<<<<<<< HEAD
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
=======
import seaborn as sns

def make_layered_hist(array, condlist, condDay):
    fig, ax = plt.subplots()
    for cond in condlist:
        hist_kde=sns.distplot(array[cond], ax=ax, label=cond)
        ax.legend()
        ax.set_xlabel('Distance Error (pixels)')
        hist_kde=hist_kde.get_figure()
        hist_kde.savefig('figs/react_hist_kde' + condDay + '.png')
>>>>>>> 3d4fa542af18c1eb83ac59f51122de37b4a45030
