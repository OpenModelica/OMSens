import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm   # for logarithmic scale
import matplotlib.ticker                   # to set a special formatter for the ticks in the colorbar (10^1 instead of 0.000(...)*10^11)
import pandas as pd
import numpy as np
import math
import os
import logging #en reemplazo de los prints
logger = logging.getLogger("--Heatmap Plotter--") #un logger especifico para este modulo

# Mine
import world3_specific.standard_run_params_defaults
import filesystem.files_aux


def main():
    pass
# Central function
def readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=False,rows_to_plot=False):
    linthresh = 1.0 #Since the logarithm of values close to zero tends toward infinity, a small range around zero needs to be mapped linearly. The parameter linthresh allows the user to specify the size of this range (-linthresh, linthresh). The size of this range in the colormap is set by linscale. When linscale == 1.0 (the default), the space used for the positive and negative halves of the linear range will be equal to one decade in the logarithmic range.
    # Start of code
    vars_name_to_ID_dict, params_name_to_ID_dict = varsAndParamsNamesToIDsDicts()

    logger.info("Reading matrix " +  input_matrix_path)
    data = readCSVAndPreprocessData(input_matrix_path,columns_to_plot,rows_to_plot)
    logger.info("Plotting to path " + plot_folder_path)
    plotHeatmapFromData(data,plot_folder_path,plot_title,linthresh,vars_name_to_ID_dict,params_name_to_ID_dict)
    logger.info("Writing rows and columns IDs ....")
    writeRowsAndColumnsIDs(data,plot_folder_path,vars_name_to_ID_dict,params_name_to_ID_dict)

# Aux:
def readCSVAndPreprocessData(input_matrix_path,columns_to_plot,rows_to_plot):
    data = pd.read_csv(input_matrix_path, index_col=0)
    if columns_to_plot:
        # Only plot a subindex of the columns
        data = data[columns_to_plot]
    if rows_to_plot:
        # Only plot a subindex of the rows
        data = data.ix[rows_to_plot]
    # Sort by alphabetical order and/or sum of cells
    data = sortIndicesAndOrColumns(data)
    return data
def plotHeatmapFromData(data,plot_folder_path,plot_title,linthresh,vars_name_to_ID_dict,params_name_to_ID_dict):
    ### Abbreviate parameters and vars to their IDs from world3_specific/(?).py so the info fits better in the heatmap
    # THere are many variables dicts (differentiable, not diferrentiable, differentiable extra, etc)
    abbreviated_columns = abbreviateStringsUsingDict(data.columns,vars_name_to_ID_dict)
    abbreviated_indices = abbreviateStringsUsingDict(data.index,params_name_to_ID_dict)
    # Pandas min and max
    ## COMMENTED BECAUSE NUMPY HANDLES NaNs BETTER
    # min_of_all = data.min().min()   # the first min returns a series of all the mins. The second min returns the min of the mins
    # max_of_all = data.max().max()   # the first max returns a series of all the maxs. The second max returns the max of the max
    ###### CONVERT TO NUMPY TO MASK INVALID DATA (COULND'T FIND OUT HOW TO MASK IN PANDAS)
    np_data = data.as_matrix()
    np_data = np.ma.masked_invalid(np_data)
    # Numpy's min and max
    min_of_all = np.nanmin(np_data)
    max_of_all = np.nanmax(np_data)
    # Calculate the upper and lower limits in the colorbar. This is to make both equals and in that way the middle of the colorbar, where the white color is located, is set to the value 0
    colorbar_limit_min, colorbar_limit_max = colorbarLimitsFromMinAndMax(min_of_all,max_of_all)


    ### Plot using logarithmic scale
    plot_name ="heatmap_logscale.png"
    fig,ax = initializeFigAndAx(data,abbreviated_indices,abbreviated_columns)
    plotHeatmapInLogarithmicScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max,linthresh)
    configurePlotTicks()
    postProcessingSettings(plot_title)
    saveAndClearPlot(plot_name,plot_folder_path)

    ### Plot using linear scale
    plot_name ="heatmap_linscale.png"
    fig,ax = initializeFigAndAx(data,abbreviated_indices,abbreviated_columns)
    plotHeatmapInLinearScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max)
    configurePlotTicks()
    postProcessingSettings(plot_title)
    saveAndClearPlot(plot_name,plot_folder_path)

def writeRowsAndColumnsIDs(data,plot_folder_path,vars_name_to_ID_dict,params_name_to_ID_dict):
    # Write Rows IDs to file
    names_list = data.index
    first_line_str = "Rows IDs:"
    rows_ids_references = os.path.join(plot_folder_path,"rows_ids.txt")
    writeIDsToFile(first_line_str,names_list,params_name_to_ID_dict,rows_ids_references)

    # Write Columns IDs to file
    names_list = data.columns
    first_line_str = "Columns IDs:"
    columns_ids_references = os.path.join(plot_folder_path,"columns_ids.txt")
    writeIDsToFile(first_line_str,names_list,vars_name_to_ID_dict,columns_ids_references)
# Function to rotate ticks labels and hide ticks
def configurePlotTicks():
    # Rotate the ticks labels in the x and y axis
    # plt.xticks(rotation=80)
    plt.xticks(rotation=90)
    # plt.yticks(rotation=-15)
    plt.yticks(rotation=0)


    # Turn off all the ticks
    ax = plt.gca()

    for t in ax.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
    for t in ax.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
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

def absForPossibleNaNs(number):
    abs_res = 0 if np.isnan(number) else abs(number)
    return abs_res

def sortIndicesAndOrColumns(data):
    ### Sort indices by sum of absolute values:
      # Create a new column with the sum of the absolute values
    data["abs_sum"] = data.apply(lambda x: sum([absForPossibleNaNs(x[col]) for col in data.columns]),axis=1)
      # Sort by that column and delete the column (both sort and drop return a new dataframe, so to minimize code lines i put them together)
    data = data.sort_values("abs_sum",ascending=False).drop("abs_sum",axis=1)

    ### Sort data's indices by alphabetical order
    # data.sort_index(inplace=True)
    ### Sort data's columns by alphabetical order
    data.sort_index(axis=1,inplace=True)
    return data


def saveAndClearPlot(plot_name,plot_folder_path):
    # plt.show()
    plot_path = os.path.join(plot_folder_path,plot_name)
    plt.savefig(plot_path,bbox_inches='tight')
    plt.clf()

def initializeFigAndAx(data,abbreviated_indices,abbreviated_columns):
    # Plot it out
    fig, ax = plt.subplots()

    # Set xlim and ylim manually because matplotlib has an internal bug that adds empty columns and rows because it thinks (wrongly) that there are n+1 rows and m+1 columns
    ax.set_ylim(0,len(data.index))
    ax.set_xlim(0,len(data.columns))


    ### Draw an "X" on invalid values (need to be masked so pcolor makes them transparent and the frame has to be set)
    ax.patch.set(hatch='x', edgecolor='blue')

    # Format
    fig.set_size_inches(10, 11)

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

    ax.grid(False)
    return fig,ax
def plotHeatmapInLogarithmicScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max,linthresh):
    # Logarithmic scale
    # heatmap = ax.pcolor(np_data, cmap=plt.cm.Blues, norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # heatmap = ax.pcolor(np_data,vmin=colorbar_limit_min, vmax=colorbar_limit_max,  norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # heatmap = ax.pcolor(np_data, cmap=plt.cm.Blues, norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # heatmap = ax.pcolor(np_data, cmap=plt.cm.seismic, norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    heatmap = ax.pcolor(np_data, cmap=plt.cm.bwr, norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # heatmap = ax.pcolor(np_data,  norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # The ticks of the colorbar are all powers of 10 and also the min and the max of the heatmap
    colorbar_ticks = list(set(exponentialRangeFromMinAndMax(colorbar_limit_min,colorbar_limit_max) + [colorbar_limit_min,colorbar_limit_max])) # list(set(...)) so the duplicates are eliminated
    cbar = fig.colorbar(heatmap,ticks=colorbar_ticks,format=matplotlib.ticker.FuncFormatter(lambda x,p: logTickerToString(x,p))) # I create a lambda instead of just putting the function name so it's more explicit that it's a function and that it receives x and p
    # Change font size in color bar
    cbar.ax.tick_params(labelsize=10)

def plotHeatmapInLinearScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max):
    # Linear scale:
    # BORRAR
    # heatmap = ax.pcolor(np_data)
    heatmap = ax.pcolor(np_data, cmap=plt.cm.bwr,vmin=colorbar_limit_min,vmax=colorbar_limit_max)
    # increment = (colorbar_limit_max-colorbar_limit_min)/20  # 20 ticks
    increment = (colorbar_limit_max-colorbar_limit_min)/20  # 20 ticks
    # colorbar_ticks = [colorbar_limit_min+i*increment for i in range(0,21)] # range(0,21) because range doesn't include the upper limit in the range and we have 20 ticks
    colorbar_ticks = [colorbar_limit_min+i*increment for i in range(0,21)] # range(0,21) because range doesn't include the upper limit in the range and we have 20 ticks
    # if colorbar_limit_min < 0 and 0 < colorbar_limit_max:
    #     colorbar_ticks = list(set(colorbar_ticks+[0]))   # list(set(...)) so the duplicates are eliminated


    cbar = fig.colorbar(heatmap,ticks=colorbar_ticks)

    # Change font size in color bar
    cbar.ax.tick_params(labelsize=10)
def postProcessingSettings(plot_title):
    # Plot title
    plt.title(plot_title,y=1.08) # change y=... Because the inverted tick labels bug matplotlib and the title and the tick labels are superimposed

    # Tight layout to maximize usage of space
    plt.tight_layout()
    # plt.tight_layout(rect= [0, 0.03, 1, 0.95])
def logTickerToString(x,p):
    if x==0:
        return "    0"
    else:
        return "%.0e" % x
def varsAndParamsNamesToIDsDicts():
    ### Variables dict
    vars_dicts = [world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_differentiableVariables_dict,world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_nonDiffVars_dict,world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_differentiableVariablesExtra_dict]
    vars_name_to_ID_dict = {}
    for d in vars_dicts:
        for k, v in d.items():  # d.items() in Python 3+
            vars_name_to_ID_dict[k] = v
    # Params dict
    params_name_to_ID_dict = world3_specific.standard_run_params_defaults.om_TheoParamSensitivity_params_dict
    return vars_name_to_ID_dict, params_name_to_ID_dict
def colorbarLimitsFromMinAndMax(min_of_all,max_of_all):
    if max_of_all > abs(min_of_all):
        colorbar_limit_max = max_of_all
        colorbar_limit_min = -max_of_all
    else:
        colorbar_limit_max = abs(min_of_all)
        colorbar_limit_min = min_of_all
    return colorbar_limit_min, colorbar_limit_max


# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
