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


def main():
    ##Example for "multipleCSVsAndVarsSimplePlot" using Vermeulen Run 2 & 3 Results.
    vars_list = ["Industrial_Investment1Industrial_Outputs_ind_cap_out_ratio", "Industrial_Investment1S_FIOA_Conss_fioa_cons_const","Industrial_Investment1S_Avg_Life_Ind_Caps_avg_life_ind_cap", "population","ppoll_index","industrial_output","nr_resources"]
    csvs_path_label_pair_list = [("/home/adanos/Documents/TPs/tesis/repos/modelica_scripts/resource/vj_run2.csv", "V&J Run 2"),
                                 ("/home/adanos/Documents/TPs/tesis/repos/modelica_scripts/resource/vj_run3.csv", "V&J Run 3"),]
    plot_title = "Vermeulen & Jong Runs 2 and 3 using modified models"
    x_range=[1900,2100]
    include_stdrun = True
    output_base_path = "/home/adanos/Documents/TPs/tesis/repos/modelica_scripts/tmp/simple_plots/"
    output_folder_path = filesystem.files_aux.makeDirFromCurrentTimestamp(output_base_path)
    extra_ticks = [1975]
    multipleCSVsAndVarsSimplePlot(vars_list,csvs_path_label_pair_list,plot_title,x_range,output_folder_path,extra_ticks,include_stdrun)


def multipleCSVsAndVarsSimplePlot(vars_list,csvs_path_label_pair_list,plot_title,x_range,output_folder_path,extra_ticks,include_stdrun=False):
    colors_list = plt.get_cmap('jet')(np.linspace(0, 1.0, len(csvs_path_label_pair_list)))
    for var_name in vars_list:
        colors_iter = iter(colors_list)
        footer_artist = setupPlt("Time",var_name,plot_title,"","")
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
        lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
        # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
        ## Settings that differ from the automatic plotter:
        plt.xlim(x_range) #set an specific x range
        plt.xticks(list(plt.xticks()[0]) + extra_ticks) # add extra ticks (1975 for vermeulen for example)
        autoscale_view(tight=None, scalex=False, scaley=True)
        print(output_folder_path)

        plot_path_without_extension = os.path.join(output_folder_path,var_name)
        saveAndClearPlt(plot_path_without_extension,lgd,footer_artist)

def plotVarsFromSweepingInfo(plot_vars,model_name,sweeping_info,plots_folder_path,plot_std_run):
    for var_name in plot_vars:
        plotVarFromSweepingInfo(var_name,model_name,sweeping_info,plots_folder_path,plot_std_run)

def plotVarFromSweepingInfo(var_name,model_name,sweeping_info,plots_folder_path,plot_std_run):
    # print(str(sweeping_info))
    plot_path_without_extension = os.path.join(plots_folder_path,var_name)
    logger_plot_str = "Plotting:\n  plotvar:{var_name}\n path:{plot_path_without_extension}".format(var_name=var_name,plot_path_without_extension=plot_path_without_extension)
    logger.debug(logger_plot_str)
    sweep_vars         = sweeping_info["sweep_vars"]
    fixed_params       = sweeping_info["fixed_params"]
    sweep_vars_str = ", ".join(sweep_vars)
    fixed_params_to_strs = [str(x) for x in fixed_params]
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
    swept_vars_full_str = "Swept parameters:\n {sweep_vars_str}".format(sweep_vars_str=sweep_vars_str)
    fixed_params_full_str = "Fixed params:\n {fixed_params_str}".format(fixed_params_str=fixed_params_str)
    footer = swept_vars_full_str+"\n"+fixed_params_str
    return (title,subtitle,footer)
def plotStandardRun(var_name,color="black"):
        data = readFromCSV(_std_run_csv)
        label = "STD_RUN"
        plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = color)

def readFromCSV(file_path):
    # El que estaba antes: (no plotea para mayores de 2091 y tiene puesto el skip footer)
    # data = np.genfromtxt(file_path, delimiter=',', skip_footer=10, names=True)
    # El nuevo:
    data = np.genfromtxt(file_path, delimiter=',', names=True)
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
    footer_artist = plt.annotate(footer, (-0.01,0), (2, -40), xycoords='axes fraction', textcoords='offset points', va='top', horizontalalignment='right')
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

