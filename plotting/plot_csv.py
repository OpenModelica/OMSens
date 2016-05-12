import os
import logging #en reemplazo de los prints
logger = logging.getLogger("--CSV Plotter--") #un logger especifico para este modulo
import numpy as np
import matplotlib.pyplot as plt
import matplotlib #for configuration

import settings.settings_world3_sweep as world3_settings

#GLOBALS:
_std_run_csv = world3_settings._std_run_csv 


def main():
    pass

def plotVarsFromSweepingInfo(plot_vars,model_name,sweeping_info,plots_folder_path):
    for var_name in plot_vars:
        plotVarFromSweepingInfo(var_name,model_name,sweeping_info,plots_folder_path)

def plotVarFromSweepingInfo(var_name,model_name,sweeping_info,plots_folder_path):
    plot_path_without_extension = os.path.join(plots_folder_path,var_name)
    logger_plot_str = "Plotting:\n  plotvar:{var_name}\n path:{plot_path_without_extension}".format(var_name=var_name,plot_path_without_extension=plot_path_without_extension)
    logger.debug(logger_plot_str)
    sweep_vars         = sweeping_info["sweep_vars"]
    sweep_vars_str = ", ".join(sweep_vars)
    title,subtitle,footer = sweepingPlotTexts(model_name,var_name,sweep_vars_str)
    per_iter_info_dict = sweeping_info["per_iter_info_dict"]
    footer_artist = setupPlt("Time",var_name,title,subtitle,footer)
    iterations = per_iter_info_dict.keys()
    colors = plt.get_cmap('jet')(np.linspace(0, 1.0, len(iterations)))

    # plotStandardRun(var_name,colors)

    for i in iterations:
        iter_dict = per_iter_info_dict[i]
        file_path = iter_dict["file_path"]
        data = readFromCSV(file_path)
        sweep_value = iter_dict["sweep_value"]
        label = "val={sweep_value}".format(sweep_value=sweep_value)
        plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = colors[i])
    lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
    # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
    saveAndClearPlt(plot_path_without_extension,lgd,footer_artist)
def sweepingPlotTexts(model_name,var_name,sweep_vars_str):
    title = "Sweeping Plot for model: {model_name}".format(model_name=model_name)
    subtitle ="Plotting var: {var_name}".format(var_name=var_name)
    footer = "Swept variables:\n {sweep_vars_str}".format(sweep_vars_str=sweep_vars_str)
    return (title,subtitle,footer)
def plotStandardRun(var_name,colors):
        data = readFromCSV(_std_run_csv)
        label = "STD_RUN"
        plt.plot(data["time"], data[var_name], linewidth=1, linestyle='-', markersize=0,marker='o',label=label,color = "black")
def plotVarFromCSVs(var_name,csvs_list,plot_path, plot_title):
    # IMPORTANT: needs fix with new setupPlt!!! (doesn't work)
    logger_plot_str = "Plotting:\n  plotvar:{var_name}\n  csvs:{csvs_list}\n path:{plot_path}".format(var_name=var_name,csvs_list=csvs_list,plot_path=plot_path)
    logger.debug(logger_plot_str)
    setupPlt("Time","f(x)",plot_title)

    for file_path in csvs_list:
        data = readFromCSV(file_path)
        file_name= file_path.split("/")[-1] #Creo que no funciona en MS-Win (barra distinta en paths)
        label = "{prefix}_{suffix}".format(prefix=var_name,suffix=file_name)
        plt.plot(data["time"], data[var_name], linewidth=0.5, linestyle='-', markersize=0,marker='o',label=label )
        # plt.plot(data["time"], data[var_name],label=label )
        # plt.legend(loc="best",fontsize="small")
    # plt.grid() # the style_sheet already includes a grid
    # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(1,0.5)) #A la derecha
    lgd = plt.legend(loc="center left", bbox_to_anchor=(1,0.5)) #A la derecha
    # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
    saveAndClearPlt(plot_path,lgd)


def readFromCSV(file_path):
    data = np.genfromtxt(file_path, delimiter=',', skip_footer=10, names=True)
    return data

def setupPlt(x_label,y_label,title,subtitle,footer):
# def setupPlt(x_label,y_label,title):
    # matplotlib.rcParams.update({'figure.autolayout': True})
    # plt.style.use('ggplot')
    plt.style.use('fivethirtyeight')
    plt.gca().set_position([0.10, 0.15, 0.80, 0.77])
    plt.xlabel(x_label)
    plt.title(title+"\n"+subtitle, fontsize=14)
    # plt.title(title)
    plt.ylabel(y_label)
    footer_artist = plt.annotate(footer, (0,0), (0, -40), xycoords='axes fraction', textcoords='offset points', va='top')
    # fig = plt.figure()
    # fig.text(.1,.1,footer)
    # plt.figtext(.1,.1,footer)
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

