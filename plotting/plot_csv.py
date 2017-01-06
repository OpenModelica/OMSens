import re
import os
import logging #en reemplazo de los prints
logger = logging.getLogger("--CSV Plotter--") #un logger especifico para este modulo
import numpy as np
import matplotlib.pyplot as plt
import matplotlib #for configuration
import filesystem.files_aux

import settings.settings_world3_sweep as world3_settings

#GLOBALS:
_std_run_csv = world3_settings._std_run_csv


def multipleCSVsAndVarsSimplePlotTemp(vars_list,csvs_path_label_pair_list,plot_title,x_range,output_folder_path,extra_ticks,include_stdrun=False,subtitle="",footer=""):
    colors_list = plt.get_cmap('jet')(np.linspace(0, 1.0, len(csvs_path_label_pair_list)))
    for var_name in vars_list:
        colors_iter = iter(colors_list)
        footer_artist = setupPlt("Time",var_name,plot_title,subtitle,footer)
        if include_stdrun:
            plotStandardRun(var_name)
        # for i in iterations:

        i=0 #for the colours
        for csv_path in csvs_path_label_pair_list:
            # iter_dict = per_iter_info_dict[i]
            # file_path = iter_dict["file_path"]
            # data = readFromCSV(file_path)
            data = readFromCSVTemp(csv_path)
            # sweep_value = iter_dict["sweep_value"]
            # label = "val={sweep_value}".format(sweep_value=sweep_value)
            plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',color = next(colors_iter))
            # plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = "black")
            i=i+1 #for the colours
        lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
        # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
        ## Settings that differ from the automatic plotter:
        plt.xlim(x_range) #set an specific x range
        plt.xticks(list(plt.xticks()[0]) + extra_ticks) # add extra ticks (1975 for vermeulen for example)
        print(output_folder_path)

        plot_path_without_extension = os.path.join(output_folder_path,var_name)
        saveAndClearPlt(plot_path_without_extension,lgd,footer_artist)
def multipleCSVsAndVarsSimplePlot(vars_list,csvs_path_label_pair_list,plot_title,x_range,output_folder_path,extra_ticks,include_stdrun=False,subtitle="",footer=""):
    colors_list = plt.get_cmap('jet')(np.linspace(0, 1.0, len(csvs_path_label_pair_list)))
    for var_name in vars_list:
        colors_iter = iter(colors_list)
        footer_artist = setupPlt("Time",var_name,plot_title,subtitle,footer)
        if include_stdrun:
            plotStandardRun(var_name)
        # for i in iterations:

        i=0 #for the colours
        for csv_path,label in csvs_path_label_pair_list:
            # iter_dict = per_iter_info_dict[i]
            # file_path = iter_dict["file_path"]
            # data = readFromCSV(file_path)
            data = readFromCSV(csv_path)
            # sweep_value = iter_dict["sweep_value"]
            # label = "val={sweep_value}".format(sweep_value=sweep_value)
            plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = next(colors_iter))
            # plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = "black")
            i=i+1 #for the colours
        # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
        # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
        ## Settings that differ from the automatic plotter:
        plt.xlim(x_range) #set an specific x range
        plt.xticks(list(plt.xticks()[0]) + extra_ticks) # add extra ticks (1975 for vermeulen for example)
        print(output_folder_path)

        plot_path_without_extension = os.path.join(output_folder_path,var_name)
        saveAndClearPlt(plot_path_without_extension,lgd,footer_artist)

def plotVarsFromIterationsInfo(plot_vars,model_name,iterationsInfo_list,plots_folder_path,plot_std_run,fixed_params_str,extra_ticks):
    for var_name in plot_vars:
        plotVarFromIterationsInfo(var_name,model_name,iterationsInfo_list,plots_folder_path,plot_std_run,fixed_params_str,extra_ticks)

def plotVarsFromSweepingInfo(plot_vars,model_name,sweeping_info,plots_folder_path,plot_std_run,fixed_params_str):
    for var_name in plot_vars:
        plotVarFromSweepingInfo(var_name,model_name,sweeping_info,plots_folder_path,plot_std_run,fixed_params_str)

def plotVarFromIterationsInfo(var_name,model_name,iterationsInfo_list,plots_folder_path,plot_std_run,fixed_params_str,extra_ticks):
    plot_path_without_extension = os.path.join(plots_folder_path,var_name)
    logger_plot_str = "Plotting:\n  plotvar:{var_name}\n path:{plot_path_without_extension}".format(var_name=var_name,plot_path_without_extension=plot_path_without_extension)
    logger.debug(logger_plot_str)
    swept_params_str = sweptParamsStrMultiparam(iterationsInfo_list)
    title,subtitle,footer = sweepingPlotTexts(model_name,var_name,swept_params_str,fixed_params_str)
    footer_artist = setupPlt("Time",var_name,title,subtitle,footer)
    # per_iter_info_dict = sweeping_info["per_iter_info_dict"]
    # iterations = per_iter_info_dict.keys()
    # colors = plt.get_cmap('jet')(np.linspace(0, 1.0, len(iterations)))
    colors_list = plt.get_cmap('jet')(np.linspace(0, 1.0, len(iterationsInfo_list)))
    colors_iter = iter(colors_list)

    if plot_std_run:
        plotStandardRun(var_name)

    # for i in iterations:
    for iterInfo in iterationsInfo_list:
        file_path = iterInfo.csv_path
        data = readFromCSV(file_path)
        label = labelForIterInfo(iterInfo)
        plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = next(colors_iter))
    lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
    # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
    setupXTicks(extra_ticks)
    saveAndClearPlt(plot_path_without_extension,lgd,footer_artist)

def setupXTicks(extra_ticks):
    # Get the ticks automatically generated by matplotlib
    auto_x_ticks = list(plt.xticks()[0]) 
    # Trim the borders (excessively large)
    auto_x_ticks_wo_borders =  auto_x_ticks[1:-1]
    x_ticks = sorted(auto_x_ticks_wo_borders + extra_ticks)
    plt.xticks(x_ticks,rotation='vertical') # add extra ticks (1975 for vermeulen for example)

def labelForIterInfo(iterInfo):
    simu_param_info_list = iterInfo.simu_param_info_list
    params_strs_list = []
    for param_pos in range(0,len(simu_param_info_list)):
        simu_param_info = simu_param_info_list[param_pos]
        param_name = simu_param_info.param_name
        this_run_val = simu_param_info.this_run_val
        this_run_def_diff = simu_param_info.this_run_def_diff
        param_id_str = "({id})".format(id=param_pos)
        param_str = "{param_id_str}={val:.2f} [{def_diff}]".format(param_id_str=param_id_str,val=this_run_val,def_diff=this_run_def_diff)
        params_strs_list.append(param_str)
    label = " | ".join(params_strs_list)
    return label

def plotVarFromSweepingInfo(var_name,model_name,sweeping_info,plots_folder_path,plot_std_run,fixed_params_str):
    # print(str(sweeping_info))
    plot_path_without_extension = os.path.join(plots_folder_path,var_name)
    logger_plot_str = "Plotting:\n  plotvar:{var_name}\n path:{plot_path_without_extension}".format(var_name=var_name,plot_path_without_extension=plot_path_without_extension)
    logger.debug(logger_plot_str)
    sweep_vars         = sweeping_info["sweep_vars"]
    fixed_params       = sweeping_info["fixed_params"]
    sweep_vars_str = ", ".join(sweep_vars)
    fixed_params_to_strs = [str(x) for x in fixed_params]
    if fixed_params_str == False:
        fixed_params_str = ", ".join(fixed_params_to_strs)
    title,subtitle,footer = sweepingPlotTexts(model_name,var_name,sweep_vars_str,fixed_params_str)
    per_iter_info_dict = sweeping_info["per_iter_info_dict"]
    footer_artist = setupPlt("Time",var_name,title,subtitle,footer)
    iterations = per_iter_info_dict.keys()
    # colors = plt.get_cmap('jet')(np.linspace(0, 1.0, len(iterations)))
    colors_list = plt.get_cmap('jet')(np.linspace(0, 1.0, len(iterations)))
    colors_iter = iter(colors_list)

    if plot_std_run:
        plotStandardRun(var_name)

    for i in iterations:
        iter_dict = per_iter_info_dict[i]
        file_path = iter_dict["file_path"]
        data = readFromCSV(file_path)
        sweep_value = iter_dict["sweep_value"]
        label = "param_val={sweep_value:.2f}".format(sweep_value=sweep_value)
        plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = next(colors_iter))
    lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
    # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
    saveAndClearPlt(plot_path_without_extension,lgd,footer_artist)
def sweepingPlotTexts(model_name,var_name,sweep_vars_str,fixed_params_str):
    title = "Sweeping Plot for model: {model_name}".format(model_name=model_name)
    subtitle ="Plotting var: {var_name}".format(var_name=var_name)
    swept_vars_full_str = "Swept parameters:  \n {sweep_vars_str}".format(sweep_vars_str=sweep_vars_str)
    fixed_params_full_str = "Fixed params:  \n {fixed_params_str}".format(fixed_params_str=fixed_params_str)
    footer = swept_vars_full_str+"\n"+fixed_params_full_str
    return (title,subtitle,footer)

def sweptParamsStrMultiparam(iterationsInfo_list):
    # Get the parameters list from the first iterationsInfo
    swept_params = iterationsInfo_list[0].swept_params
    # Prepare the string by joining with a comma the parameters with their ID. eg: "param_1 (1), param_2 (2) ..."
    swept_params_str = ", ".join([swept_params[i] + " ({i})".format(i=i) for i in range(0,len(swept_params))])
    return swept_params_str
def plotStandardRun(var_name,color="black"):
        data = readFromCSV(_std_run_csv)
        label = "STD_RUN"
        plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = color)

def readFromCSVTemp(file_path):
    # El que manda todo a memoria:
    # data = np.genfromtxt(file_path, delimiter=',', names=True)
    # El que no manda todo a memoria:
    print("Reading with low ram usage")
    data = np.memmap(file_path, delimiter=',', names=True)
    return data
def readFromCSV(file_path):
    # El que manda todo a memoria:
    data = np.genfromtxt(file_path, delimiter=',', names=True)
    # El que no manda todo a memoria:
    # data = np.memmap(file_path, delimiter=',', names=True)
    return data

def setupPlt(x_label,y_label,title,subtitle,footer):
# def setupPlt(x_label,y_label,title):
    # matplotlib.rcParams.update({'figure.autolayout': True})
    # plt.style.use('ggplot')
    plt.style.use('fivethirtyeight')
    plt.gca().set_position([0.10, 0.15, 0.80, 0.77])
    plt.xlabel(x_label)
    plt.title(title+"\n"+subtitle, fontsize=14, y=1.08)
    # plt.title(title)
    plt.ylabel(y_label)
    plt.ticklabel_format(useOffset=False) # So it doesn't use an offset on the x axis
    footer_artist = plt.annotate(footer, (1,0), (0, -70), xycoords='axes fraction', textcoords='offset points', va='top', horizontalalignment='right')
    # fig = plt.figure()
    # fig.text(.1,.1,footer)
    # plt.figtext(.1,.1,footer)
    plt.margins(x=0.1, y=0.1) #increase buffer so points falling on it are plotted
    return footer_artist

def saveAndClearPlt(plot_path_without_extension,lgd,footer_artist):
    # plt.savefig(plot_path)
    extensions = [".svg",".png"]
    for ext in extensions:
        plot_path = plot_path_without_extension + ext
        plt.savefig(plot_path,bbox_extra_artists=(lgd,footer_artist), bbox_inches='tight')
    # plt.show()
    plt.clf()

if __name__ == "__main__":
    main()

