import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm   # for logarithmic scale
import matplotlib.ticker                   # to set a special formatter for the ticks in the colorbar (10^1 instead of 0.000(...)*10^11)
import pandas as pd
import numpy as np
import math
import os

# Mine
import world3_specific.standard_run_params_defaults
import filesystem.files_aux

##### THIS MODULE WAS MADE ON A RUSH AND NEEDS BEAUTIFICATION      ################

# GLOBALS
# input_matrix_path = "resource/w3_only1992_time_fix_paramvarmatrix.csv"
# plot_name = "asd_sin_sort.png"

linthresh = 1.0 #Since the logarithm of values close to zero tends toward infinity, a small range around zero needs to be mapped linearly. The parameter linthresh allows the user to specify the size of this range (-linthresh, linthresh). The size of this range in the colormap is set by linscale. When linscale == 1.0 (the default), the space used for the positive and negative halves of the linear range will be equal to one decade in the logarithmic range.

def main():
    base_path = filesystem.files_aux.makeOutputPath("heatmaps")
    # omTheoParamSens_1901_all_Heatmap(base_path)
    # omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    asd(base_path)

### Special Heatmaps
# All params and vars for 1901 sens
def omTheoParamSens_1901_all_Heatmap(base_path):
    input_matrix_path = "resource/w3_only1901_time_fix_paramvarmatrix.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nAll variables and parameters from Sensitivity Analysis"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_all_Heatmap")
    os.makedirs(plot_folder_path)
    readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)

# Workpackage1 params and vars for 1901 sens
def omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    input_matrix_path = "resource/w3_only1901_time_fix_paramvarmatrix.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nOnly the variables and parameters studied in WorkPackage 1"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap")
    os.makedirs(plot_folder_path)
    readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)


# Aux:
# Function to write txts with "ID & Name" lines for the columns and indices of the heatmap
def writeIDsToFile(first_line_str,names_list,ids_dict,file_path):
    strs_list = [first_line_str]
    for name in names_list:
        id_and_name_str = ids_dict[name] + " & " + name
        strs_list.append(id_and_name_str)
    ids_to_name_str = "\n".join(strs_list)
    filesystem.files_aux.writeStrToFile(ids_to_name_str,file_path)
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

# Central function
def readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=False,rows_to_plot=False):
    plot_name = "heatmap.png"
    plot_IDs_reference_file_name = "IDs_references.txt"
    linthresh = 1.0 #Since the logarithm of values close to zero tends toward infinity, a small range around zero needs to be mapped linearly. The parameter linthresh allows the user to specify the size of this range (-linthresh, linthresh). The size of this range in the colormap is set by linscale. When linscale == 1.0 (the default), the space used for the positive and negative halves of the linear range will be equal to one decade in the logarithmic range.
    # Start of code
    data = pd.read_csv(input_matrix_path, index_col=0)
    if columns_to_plot:
        # Only plot a subindex of the columns
        data = data[columns_to_plot]
    if rows_to_plot:
        # Only plot a subindex of the rows
        data = data.ix[rows_to_plot]

    ### Sort indices by sum of absolute values:
      # Create a new column with the sum of the absolute values
    data["abs_sum"] = data.apply(lambda x: sum([absForPossibleNaNs(x[col]) for col in data.columns]),axis=1)
      # Sort by that column and delete the column (both sort and drop return a new dataframe, so to minimize code lines i put them together)
    data = data.sort_values("abs_sum",ascending=False).drop("abs_sum",axis=1)

    ### Sort data's indices by alphabetical order
    # data.sort_index(inplace=True)
    ### Sort data's columns by alphabetical order
    data.sort_index(axis=1,inplace=True)

    ### Abbreviate parameters and vars to their IDs from world3_specific/(?).py so the info fits better in the heatmap
    abbreviated_columns = abbreviateStringsUsingDict(data.columns,world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_differentiableVariables_dict)
    abbreviated_indices = abbreviateStringsUsingDict(data.index,world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_params_dict)

    # Plot it out
    fig, ax = plt.subplots()

    # Set xlim and ylim manually because matplotlib has an internal bug that adds empty columns and rows because it thinks (wrongly) that there are n+1 rows and m+1 columns
    ax.set_ylim(0,len(data.index))
    ax.set_xlim(0,len(data.columns))
    min_of_all = data.min().min()   # the first min returns a series of all the mins. The second min returns the min of the mins
    max_of_all = data.max().max()   # the first max returns a series of all the maxs. The second max returns the max of the max
    ###### CONVERT TO NUMPY TO MASK INVALID DATA (COULND'T FIND OUT HOW TO MASK IN PANDAS)
    np_data = data.as_matrix()
    np_data = np.ma.masked_invalid(np_data)
    # Logarithmic scale
    # heatmap = ax.pcolor(np_data, cmap=plt.cm.Blues, norm=SymLogNorm(vmin=min_of_all, vmax=max_of_all,linthresh=linthresh))
    # heatmap = ax.pcolor(np_data,vmin=min_of_all, vmax=max_of_all,  norm=SymLogNorm(vmin=min_of_all, vmax=max_of_all,linthresh=linthresh))
    heatmap = ax.pcolor(np_data,  norm=SymLogNorm(vmin=min_of_all, vmax=max_of_all,linthresh=linthresh))
    colorbar_ticks = exponentialRangeFromMinAndMax(min_of_all,max_of_all)
    cbar = fig.colorbar(heatmap,ticks=colorbar_ticks,format=matplotlib.ticker.FuncFormatter(lambda x, p: "%.0e" % x))

    # Linear scale:
    # heatmap = ax.pcolor(np_data, cmap=plt.cm.seismic, vmin=np.nanmin(np_data), vmax=np.nanmax(np_data))
    # cbar = fig.colorbar(heatmap)

    # Change font size in color bar
    cbar.ax.tick_params(labelsize=10)

    ### Draw an "X" on invalid values (need to be masked so pcolor makes them transparent and the frame has to be set)
    ax.patch.set(hatch='x', edgecolor='blue')

    # Format
    fig = plt.gcf()
    fig.set_size_inches(8, 11)

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

    # Plot title
    plt.title(plot_title,y=1.05)

    # Tight layout to maximize usage of space
    plt.tight_layout()
    # plt.tight_layout(rect= [0, 0.03, 1, 0.95])

    plt.show()
    # plot_path = os.path.join(plot_folder_path,plot_name)
    # plt.savefig(plot_path)

    # Write Rows IDs to file
    ids_dict = world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_params_dict
    names_list = data.index
    first_line_str = "Rows IDs:"
    rows_ids_references = os.path.join(plot_folder_path,"rows_ids.txt")
    writeIDsToFile(first_line_str,names_list,ids_dict,rows_ids_references)

    # Write Columns IDs to file
    ids_dict = world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_differentiableVariables_dict
    names_list = data.columns
    first_line_str = "Columns IDs:"
    columns_ids_references = os.path.join(plot_folder_path,"columns_ids.txt")
    writeIDsToFile(first_line_str,names_list,ids_dict,columns_ids_references)

def absForPossibleNaNs(number):
    abs_res = 0 if np.isnan(number) else abs(number)
    return abs_res


# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
