import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm   # for logarithmic scale
import pandas as pd
import numpy as np

# GLOBALS
input_matrix_path = "resource/w3_only1992_time_fix_paramvarmatrix.csv"
linthresh = 1.0 #Since the logarithm of values close to zero tends toward infinity, a small range around zero needs to be mapped linearly. The parameter linthresh allows the user to specify the size of this range (-linthresh, linthresh). The size of this range in the colormap is set by linscale. When linscale == 1.0 (the default), the space used for the positive and negative halves of the linear range will be equal to one decade in the logarithmic range.

# page = urlopen("http://datasets.flowingdata.com/ppg2008.csv")
# data = pd.read_csv("asd.csv", index_col=0)
data = pd.read_csv(input_matrix_path, index_col=0)
# nba = pd.read_csv(page, index_col=0)

# Normalize data columns
# nba_norm = (nba - nba.mean()) / (nba.max() - nba.min())

# Sort data according to Points, lowest to highest
# This was just a design choice made by Yau
# inplace=False (default) ->thanks SO user d1337

# Plot it out
print(str(data.min()))
print(str(data.max()))
fig, ax = plt.subplots()
min_of_all = data.min().min()   # the first min returns a series of all the mins. The second min returns the min of the mins
max_of_all = data.max().max()   # the first max returns a series of all the max. The second max returns the max of the max
heatmap = plt.pcolor(data, norm=SymLogNorm(vmin=min_of_all, vmax=max_of_all,linthresh=linthresh))

plt.colorbar()

# Format
fig = plt.gcf()
fig.set_size_inches(8, 11)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

# Set the labels

# label source:https://en.wikipedia.org/wiki/Basketball_statistics
# labels = [
#     'Games', 'Minutes', 'Points', 'Field goals made', 'Field goal attempts', 'Field goal percentage', 'Free throws made', 'Free throws attempts', 'Free throws percentage',
    # 'Three-pointers made', 'Three-point attempt', 'Three-point percentage', 'Offensive rebounds', 'Defensive rebounds', 'Total rebounds', 'Assists', 'Steals', 'Blocks', 'Turnover', 'Personal foul']

# note I could have used nba_sort.columns but made "labels" instead
ax.set_xticklabels(data.columns, minor=False)
ax.set_yticklabels(data.index, minor=False)

# rotate the
plt.xticks(rotation=90)

ax.grid(False)

# Turn off all the ticks
ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

plt.show()
