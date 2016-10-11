import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm   # for logarithmic scale
import matplotlib.ticker                   # to set a special formatter for the ticks in the colorbar (10^1 instead of 0.000(...)*10^11)
import pandas as pd
import numpy as np
import math
import os

# Mine
import world3_specific.standard_run_params_defaults

##### THIS MODULE WAS MADE ON A RUSH AND NEEDS BEAUTIFICATION      ################

# GLOBALS
input_matrix_path = "resource/w3_only1992_time_fix_paramvarmatrix.csv"
# input_matrix_path = "resource/w3_only1901_time_fix_paramvarmatrix.csv"
plot_folder_path = "tmp"
# plot_name = "asd_sin_sort.png"
plot_name = "asd_con_sort.png"

linthresh = 1.0 #Since the logarithm of values close to zero tends toward infinity, a small range around zero needs to be mapped linearly. The parameter linthresh allows the user to specify the size of this range (-linthresh, linthresh). The size of this range in the colormap is set by linscale. When linscale == 1.0 (the default), the space used for the positive and negative halves of the linear range will be equal to one decade in the logarithmic range.

# Aux:
# Function to abbreviate variables and parameters to their id ("population" -> "V.103")
def abbreviateStringsUsingDict(strs_list,abbr_dict):
    abbreviated_indices = []
    for long_str in strs_list:
        abbreviated_indices.append(abbr_dict[long_str])
    return abbreviated_indices

# Function to get numbers in an exponential range (used in the ticks in the colorbar of the colormap)
def exponentialRangeFromMinAndMax(min_num,max_num):
    res_range = []
    if min_num == 0:
        largest_positive_power_of_ten_smaller_than_min = 0
    else:
        min_SymLog = math.floor(math.log10(min_num)) if min_num > 0 else math.floor(math.log10(abs(min_num))) # symlog because it can take negative numbers
        if min_SymLog <0:
            # The number is between -1 and 0 or between 0 and 1
            if min_num <0:
                # -1 < number < 0
                largest_positive_power_of_ten_smaller_than_min = -1
            else:
                # 0 < number < 1
                largest_positive_power_of_ten_smaller_than_min = 0
        else:
            # number <= -1 or 1 <= number
            largest_positive_power_of_ten_smaller_than_min = math.copysign(10**min_SymLog,min_num)
    if max_num == 0:
        smallest_power_of_ten_larger_than_max = 0
    else:
        max_SymLog = math.ceil(math.log10(max_num)) if max_num > 0 else math.ceil(math.log10(abs(max_num))) # symlog because it can take negative numbers
        if max_SymLog <0:
            # The number is between -1 and 0 or between 0 and 1
            if max_num <0:
                # -1 < number < 0
                smallest_power_of_ten_larger_than_max = 0
            else:
                # 0 < number < 1
                smallest_power_of_ten_larger_than_max= 1
        else:
            # number <= -1 or 1 <= number
            smallest_power_of_ten_larger_than_max = math.copysign(10**max_SymLog,max_num)
    accum = largest_positive_power_of_ten_smaller_than_min
    while accum <= smallest_power_of_ten_larger_than_max:
        while accum <= -1:
            res_range.append(accum)
            accum = accum/10
        if accum <= smallest_power_of_ten_larger_than_max:
            res_range.append(0)
            accum = 1
            while accum <= smallest_power_of_ten_larger_than_max:
                res_range.append(accum)
                accum = accum*10
    return res_range
# Start of code
data = pd.read_csv(input_matrix_path, index_col=0)

# Sort data's indices
data.sort_index(inplace=True)
# Sort data's columns
data.sort_index(axis=1,inplace=True)

### Abbreviate parameters and vars to their IDs from world3_specific/(?).py so the info fits better in the heatmap
abbreviated_columns = abbreviateStringsUsingDict(data.columns,world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_differentiableVariables_dict)
abbreviated_indices = abbreviateStringsUsingDict(data.index,world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_params_dict)

# Plot it out
fig, ax = plt.subplots()
min_of_all = data.min().min()   # the first min returns a series of all the mins. The second min returns the min of the mins
max_of_all = data.max().max()   # the first max returns a series of all the maxs. The second max returns the max of the max
heatmap = plt.pcolor(data, norm=SymLogNorm(vmin=min_of_all, vmax=max_of_all,linthresh=linthresh))
colorbar_ticks = exponentialRangeFromMinAndMax(min_of_all,max_of_all)

cbar = plt.colorbar(ticks=colorbar_ticks,format=matplotlib.ticker.FuncFormatter(lambda x, p: "%.0e" % x))
cbar.ax.tick_params(labelsize=10)

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

## With long string names
# ax.set_xticklabels(data.columns, minor=False)
# ax.set_yticklabels(data.index, minor=False)
## With abbreviated string names
ax.set_xticklabels(abbreviated_columns, minor=False, fontsize=8)
ax.set_yticklabels(abbreviated_indices, minor=False, fontsize=6)

# Rotate the ticks labels in the x and y axis
# plt.xticks(rotation=80)
plt.xticks(rotation=90)
# plt.yticks(rotation=-15)
plt.yticks(rotation=0)

ax.grid(False)

# Turn off all the ticks
ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

# Tight layout to maximize usage of space
plt.tight_layout()

# plt.show()
plot_path = os.path.join(plot_folder_path,plot_name)
plt.savefig(plot_path)
