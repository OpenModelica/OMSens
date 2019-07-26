import logging  # en reemplazo de los prints
import math
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches  # to add patches to "non transparent" cells
import matplotlib.pyplot as plt
import matplotlib.ticker  # to set a special formatter for the ticks in the colorbar (10^1 instead of 0.000(...)*10^11)
import numpy as np
import pandas as pd
from matplotlib.colors import SymLogNorm  # for logarithmic scale

logger = logging.getLogger("--Heatmap Plotter--")

# Mine
import world3_specific.standard_run_params_defaults
import filesystem.files_aux


class Heatmap:
    # Instance functions
    def __init__(self, df_matrix, linthresh=1.0):
        # linthresh:
        #   Since the logarithm of values close to zero tends toward infinity, a small range around zero
        #   needs to be mapped linearly. The parameter linthresh allows the user to specify the size of this range (
        #   -linthresh, linthresh). The size of this range in the colormap is set by linscale. When linscale == 1.0 (the
        #   default), the space used for the positive and negative halves of the linear range will be equal to one decade
        #   in the logarithmic range.
        self.linthresh = linthresh
        # Save input df
        self.df_matrix_input = df_matrix
        # Manipulate input dataframe (sort columns, rows, etc)
        self.df_matrix_heatmap = self.manipulateInputDataframe(df_matrix)
        # Define index's heatmap names
        orig_index_names = self.df_matrix_heatmap.index.values.tolist()
        index_names_prefix = "P."
        self.index_names_map = shortenStringsWithPrefix(orig_index_names, index_names_prefix)
        # Define columns' heatmap names
        orig_cols_names = self.df_matrix_heatmap.columns.values.tolist()
        cols_names_prefix = "V."
        self.cols_names_map = shortenStringsWithPrefix(orig_cols_names, cols_names_prefix)
        # Define the colorbar upper and lower limits
        self.colorbar_min, self.colorbar_max = colorbarLimitsForDataFrame(self.df_matrix_heatmap)
        # Define the colors of the heatmap
        self.colormap = colorMapForDataFrame(self.df_matrix_heatmap)

    def plotInFolder(self, plot_folder_path):
        # Write the matrix used in the heatmap to file
        matrix_file_path = self.writeMatrixDFToFolderPath(plot_folder_path)
        # Get cols and index names from DF and their respective mappings
        # Index mapped names
        index_names = self.df_matrix_heatmap.index.values.tolist()
        index_names_mapped = [self.index_names_map[index_name] for index_name in index_names]
        # Columns mapped names
        cols_names = self.df_matrix_heatmap.columns.values.tolist()
        cols_names_mapped = [self.cols_names_map[col_name] for col_name in cols_names]
        # Initialize figure and axes with heatmap configurations
        fig, ax = initializeFigAndAx(self.df_matrix_heatmap, index_names_mapped, cols_names_mapped)
        # Plot heatmap in figure and ax
        heatmap_plot = ax.pcolor(self.df_matrix_heatmap, cmap=self.colormap, vmin=self.colorbar_min,
                                 vmax=self.colorbar_max)
        # Colorbar from limits
        # 20 ticks
        increment = (self.colorbar_max - self.colorbar_min) / 20

        # range(0,21) because range doesn't include the upper limit in the range and we have 20 ticks
        colorbar_ticks = [self.colorbar_min + i * increment for i in range(0, 21)]
        cbar = fig.colorbar(heatmap_plot, ticks=colorbar_ticks)
        # Change font size in color bar
        cbar.ax.tick_params(labelsize=10)
        # Save plot in folder
        plot_name = "heatmap.png"
        plot_path = os.path.join(plot_folder_path, plot_name)
        plt.savefig(plot_path, bbox_inches='tight')
        # Clear plot in case there are more plots coming
        plt.clf()

        # Write mappings to file
        df_index_mappings = dfFromDict(self.index_names_map)
        index_mapping_file_name = "index_mappings.csv"
        index_mapping_file_path = os.path.join(plot_folder_path, index_mapping_file_name)
        df_index_mappings.to_csv(index_mapping_file_path, index=False)

        df_cols_mappings = dfFromDict(self.cols_names_map)
        cols_mapping_file_name = "cols_mappings.csv"
        cols_mapping_file_path = os.path.join(plot_folder_path, cols_mapping_file_name)
        df_cols_mappings.to_csv(cols_mapping_file_path, index=False)
        # Return paths for created files
        paths_dict = {
            "plot_path": plot_path,
            "index_mapping_file_path": index_mapping_file_path,
            "cols_mapping_file_path": cols_mapping_file_path,
            "matrix_file_path": matrix_file_path,
        }
        return paths_dict

    def writeMatrixDFToFolderPath(self, plot_folder_path):
        matrix_file_name = "matrix.csv"
        matrix_file_path = os.path.join(plot_folder_path, matrix_file_name)
        self.df_matrix_heatmap.to_csv(matrix_file_path)
        return matrix_file_path

    # Auxs:
    def manipulateInputDataframe(self, df_input):
        # Make a copy of the input dataframe
        df_heatmap_tmp = df_input.copy()
        # Sort parameters
        df_heatmap_tmp = self.sortIndexBySumOfColumns(df_heatmap_tmp)
        # Sort data's columns by alphabetical order
        df_heatmap_tmp = self.sortColumnsByAlphabeticalOrder(df_heatmap_tmp)
        return df_heatmap_tmp

    def sortColumnsByAlphabeticalOrder(self, df_heatmap_tmp):
        df_heatmap_tmp = df_heatmap_tmp.sort_index(axis=1)
        return df_heatmap_tmp

    def sortIndexBySumOfColumns(self, df_heatmap_tmp):
        ### Sort indices by sum of absolute values:
        # Create a new column with the sum of the absolute values
        df_heatmap_tmp["abs_sum"] = df_heatmap_tmp.apply(
            lambda x: sum([absForPossibleNaNs(x[col]) for col in df_heatmap_tmp.columns]), axis=1)
        # Sort by that column and delete the column (both "sort" and "drop" return a new dataframe, so to minimize the lines
        # of code we put them together)
        df_heatmap_tmp = df_heatmap_tmp.sort_values("abs_sum", ascending=False).drop("abs_sum", axis=1)
        return df_heatmap_tmp

    def heatmapDataFrame(self):
        return self.df_matrix_heatmap


def initializeFigAndAx(data, rows_names, cols_names):
    # Plot it out
    fig, ax = plt.subplots()
    # Set xlim and ylim manually because matplotlib has an internal bug that adds empty columns and rows because it
    # thinks (wrongly) that there are n+1 rows and m+1 columns
    ax.set_ylim(0, len(data.index))
    ax.set_xlim(0, len(data.columns))

    # Format
    # fig.set_size_inches(10, 11)
    fig.set_size_inches(5, 5)

    # put the major ticks at the middle of each cell
    ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    # With abbreviated string names
    ax.set_xticklabels(cols_names, minor=False, rotation='vertical', fontsize=14)
    ax.set_yticklabels(rows_names, minor=False, fontsize=14)
    # Set the heatmap grid as false
    ax.grid(False)
    return fig, ax


def colorbarLimitsForDataFrame(df):
    # Get mins and maxs of any cell
    max_of_all = df.max().max()
    min_of_all = df.min().min()
    # Match the colorbar limits to the max of the absolute value of them
    if max_of_all > abs(min_of_all):
        colorbar_limit_max = max_of_all
        colorbar_limit_min = -max_of_all
    else:
        colorbar_limit_max = abs(min_of_all)
        colorbar_limit_min = min_of_all
    # Set the colorbar limit min to 0 if there are no negative numbers
    if min_of_all >= 0:
        colorbar_limit_min = 0
    return colorbar_limit_min, colorbar_limit_max


def colorMapForDataFrame(df, colors=200):
    # Choose  the color scheme:
    #    . "blue-white-red"     if there are negative numbers
    #    . "white-red"   if there are NO negative numbers
    min_of_all = df.min().min()
    if min_of_all >= 0:
        # The following is to get the default colormap and manually set white as it starting value for 0
        reds_cm = matplotlib.cm.get_cmap("Reds", colors)  # generate a predefined map with amount of  values
        red_vals = reds_cm(np.arange(colors))  # extract those values as an array
        red_vals = np.insert(red_vals, 1, [1, 1, 1, 1], axis=0)  # prepend pure white to the list
        colormap = matplotlib.colors.LinearSegmentedColormap.from_list("newReds", red_vals)
    else:
        # The following is to get the default colormap and manually set white as it starting value for 0
        colormap = matplotlib.cm.get_cmap("bwr")
    return colormap

def shortenStringsWithPrefix(orig_strs, prefix):
    # Sort the strings so they're numbered by alphabetical order
    orig_strs_sorted = sorted(orig_strs)
    # Create a dict with dict[str] = shortened_str
    strs_map = {}
    for i in range(0, len(orig_strs_sorted)):
        orig_str = orig_strs_sorted[i]
        str_id = i + 1
        shortened_str = "{0}{1}".format(prefix, str_id)
        strs_map[orig_str] = shortened_str
    return strs_map


def dfFromDict(strs_mapping):
    # Set a convention for the column names
    orig_strs_col_name = "Original"
    mapped_strs_col_name = "Shortened"
    # Make a list of dicts, one per mapping
    rows_dicts_list = []
    for orig_str, mapped_str in strs_mapping.items():
        row_dict = {orig_strs_col_name: orig_str, mapped_strs_col_name: mapped_str}
        rows_dicts_list.append(row_dict)
    # Create DF from rows_dict
    df_mapping = pd.DataFrame.from_records(rows_dicts_list)
    # Order DF with specific order
    cols_order = [mapped_strs_col_name, orig_strs_col_name]
    def_mapping_reordered = df_mapping.reindex(columns=cols_order)
    return def_mapping_reordered

# The functions from here on still need to be adapted and are deprecated:

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
    # Get mask positions of 0 values before masking NaNs so NaN cells aren't included
    cells_with_0 = np_data == 0
    cells_with_0_initialkwargs = {"width":1,"height":1,"fill":False, "edgecolor":(0,0,1,1), "snap":True, "linewidth":0.1, "hatch":'xx', "label": "Zeros"}
    # Get mask positions of NaN values explicitly so it's easier to create a Rectangle patch with these values
    cells_with_nans = np.isnan(np_data)
    cells_with_nans_initialkwargs = {"width":1,"height":1,"fill":True, "facecolor":(0.6,0.6,0.6,1), "edgecolor":'black', "linewidth":0.1, "hatch":'xx', "label": "NaNs"}

    # mask invalid data (NaNs) so the heatmap is not bugged
    np_data = np.ma.masked_invalid(np_data)
    # Numpy's min and max
    min_of_all = np.nanmin(np_data)
    max_of_all = np.nanmax(np_data)
    # Calculate the upper and lower limits in the colorbar. This is to have the 0 located in the middle and both colors
    #  of equal distribution.
    colorbar_limit_min, colorbar_limit_max = colorbarLimitsFromMinAndMax(min_of_all,max_of_all)
    #
    # Choose  the color scheme:
    #    . "blue-white-red"     if there are negative numbers
    #    . "white-red"   if there are NO negative numbers
    colormap = chooseColormapFromMin(min_of_all)

    ### Plot using logarithmic scale
    plot_name ="heatmap_logscale.png"
    fig,ax = initializeFigAndAx(data,abbreviated_indices,abbreviated_columns)
    plotHeatmapInLogarithmicScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max,linthresh,colormap)
    plotHeatmapInLinearScaleFromFigAxAndData(fig, ax, np_data, colorbar_limit_min, colorbar_limit_max, colormap)
    configurePlotTicks()
    addPatchesToEmphasizeCertainValues(ax, cells_with_0, cells_with_0_initialkwargs, cells_with_nans,
                                       cells_with_nans_initialkwargs)
    addLegendForPatches(cells_with_0_initialkwargs,cells_with_nans_initialkwargs)
    postProcessingSettings(plot_title)
    saveAndClearPlot(plot_name,plot_folder_path)

    ### Plot using linear scale
    plot_name ="heatmap_linscale.png"
    fig,ax = initializeFigAndAx(data,abbreviated_indices,abbreviated_columns)
    plotHeatmapInLinearScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max,colormap)
    configurePlotTicks()
    addPatchesToEmphasizeCertainValues(ax, cells_with_0, cells_with_0_initialkwargs, cells_with_nans,
                                       cells_with_nans_initialkwargs)
    addLegendForPatches(cells_with_0_initialkwargs,cells_with_nans_initialkwargs)
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
    # Sort by that column and delete the column (both "sort" and "drop" return a new dataframe, so to minimize the lines
    # of code we put them together)
    data = data.sort_values("abs_sum",ascending=False).drop("abs_sum",axis=1)

    ### Sort data's indices by alphabetical order
    # data.sort_index(inplace=True)
    ### Sort data's columns by alphabetical order
    data.sort_index(axis=1,inplace=True)

    # For paper heatmap (it's hardcoded because it's urgent):
    # data = data[:21]
    return data


def saveAndClearPlot(plot_name,plot_folder_path):
    # plt.show()
    plot_path = os.path.join(plot_folder_path,plot_name)
    plt.savefig(plot_path,bbox_inches='tight')

    plt.clf()

def plotHeatmapInLogarithmicScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max,linthresh,colormap):
    # Logarithmic scale
    heatmap = ax.pcolor(np_data, cmap=colormap, norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # heatmap = ax.pcolor(np_data,  norm=SymLogNorm(vmin=colorbar_limit_min, vmax=colorbar_limit_max,linthresh=linthresh))
    # The ticks of the colorbar are all powers of 10 and also the min and the max of the heatmap
    colorbar_ticks = list(set(exponentialRangeFromMinAndMax(colorbar_limit_min,colorbar_limit_max) + [colorbar_limit_min,colorbar_limit_max])) # list(set(...)) so the duplicates are eliminated
    cbar = fig.colorbar(heatmap,ticks=colorbar_ticks,format=matplotlib.ticker.FuncFormatter(lambda x,p: logTickerToString(x,p))) # I create a lambda instead of just putting the function name so it's more explicit that it's a function and that it receives x and p
    # Change font size in color bar
    cbar.ax.tick_params(labelsize=10)

def plotHeatmapInLinearScaleFromFigAxAndData(fig,ax,np_data,colorbar_limit_min,colorbar_limit_max,colormap):
    # Linear scale:
    heatmap = ax.pcolor(np_data, cmap=colormap,vmin=colorbar_limit_min,vmax=colorbar_limit_max)
    increment = (colorbar_limit_max-colorbar_limit_min)/20  # 20 ticks
    colorbar_ticks = [colorbar_limit_min+i*increment for i in range(0,21)] # range(0,21) because range doesn't include the upper limit in the range and we have 20 ticks
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
    # Match the colorbar limits to the max of the absolute value of them
    if max_of_all > abs(min_of_all):
        colorbar_limit_max = max_of_all
        colorbar_limit_min = -max_of_all
    else:
        colorbar_limit_max = abs(min_of_all)
        colorbar_limit_min = min_of_all
    # Set the colorbar limit min to 0 if there are no negative numbers
    if min_of_all >= 0:
        colorbar_limit_min = 0
    return colorbar_limit_min, colorbar_limit_max
def chooseColormapFromMin(min_of_all):
    values = 200 # how many colors
    if min_of_all >= 0:
        # The following is to get the default colormap and manually set white as it starting value for 0
        reds_cm = matplotlib.cm.get_cmap("Reds", values) #generate a predefined map with amount of  values
        red_vals = reds_cm(np.arange(values)) #extract those values as an array
        red_vals = np.insert(red_vals,1,[1,1,1,1],axis=0)  # prepend pure white to the list
        colormap = matplotlib.colors.LinearSegmentedColormap.from_list("newReds", red_vals)
    else:
        # The following is to get the default colormap and manually set white as it starting value for 0
        colormap = matplotlib.cm.get_cmap("bwr")
    return colormap


def addPatchesToEmphasizeCertainValues(ax, cells_with_0, cells_with_0_initialkwargs, cells_with_nans,
                                       cells_with_nans_initialkwargs):
    # Put an x over cells which have value NaN
    for j, i in np.column_stack(np.where(cells_with_nans)):
        copy_of_dict = dict(cells_with_nans_initialkwargs)
        copy_of_dict["xy"] = (i,j)
        ax.add_patch(mpatches.Rectangle(**copy_of_dict))
    # Put an x over cells which have value 0
    for j, i in np.column_stack(np.where(cells_with_0)):
        copy_of_dict = dict(cells_with_0_initialkwargs)
        copy_of_dict["xy"] = (i,j)
        ax.add_patch(mpatches.Rectangle(**copy_of_dict))
def addLegendForPatches(cells_with_0_initialkwargs,cells_with_nans_initialkwargs):
    copy_of_dict_0s           = dict(cells_with_0_initialkwargs)
    copy_of_dict_0s["xy"]     = (0,0)
    copy_of_dict_nans         = dict(cells_with_nans_initialkwargs)
    copy_of_dict_nans["xy"]   = (0,0)
    cells_with_0_patch_legend = mpatches.Rectangle(**copy_of_dict_0s)
    nans_legend               = mpatches.Rectangle(**copy_of_dict_nans)
    plt.legend(handles=[cells_with_0_patch_legend,nans_legend],loc="upper left", bbox_to_anchor=(1.03, 1.07))
