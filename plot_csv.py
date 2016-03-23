# import matplotlib
# matplotlib.use("SVG") # necesario para que escupa a archivo y no tire error
# import matplotlib.pyplot as plt
# import codecs
# import sys
# import os
# import subprocess
# import numpy #para usar sus arrays y sus masks
# from datetime import datetime #to get time and date for folder name
# import shutil #to copy files
# #Hack to import packages in other folders
# import inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
# from input.yearlydata import YearlyData
# from processing.datadiffer import DataDiffer
# import logging #en reemplazo de los prints
# logger = logging.getLogger("Plotter") #un logger especifico para este modulo

# variables_dict_script_path = currentdir+"/../processing/variables-dict.py"
####### Imports que seguro van:
import numpy as np
import matplotlib.pyplot as plt
def main():
    #ENTRADA:
    # csvs_list = ["BouncingBall_1_res.csv","BouncingBall_2_res.csv","BouncingBall_3_res.csv"]
    csvs_list = ["SystemDynamics.WorldDynamics.World3.Scenario_1_1_res.csv","SystemDynamics.WorldDynamics.World3.Scenario_1_2_res.csv"]
    plot_path = "tmp/plot.svg"
    var_name = "nr_resources"
    # /ENTRADA
    plotVarFromCSVs(var_name,csvs_list,plot_path)
def plotVarFromCSVs(var_name,csvs_list,plot_path):
    setupPlt("Time","f(x)","Ploteo de archivito")

    for file_path in csvs_list:
        data = readFromCSV(file_path)
        file_name= file_path.split("/")[-1]
        label = "{prefix}_{suffix}".format(prefix=var_name,suffix=file_name)
        plt.plot(data["time"], data[var_name], linewidth=0.5, linestyle='-', markersize=0,marker='o',label=label )
        # plt.legend(loc="best",fontsize="small")
        plt.legend(loc="center left",fontsize="small",bbox_to_anchor=(1,0.5))
    plt.grid()
    saveAndClearPlt(plot_path)


def readFromCSV(file_path):
    data = np.genfromtxt(file_path, delimiter=',', skip_footer=10, names=True)
    return data

# def setupPlt(x_label,y_label,title,subtitle,footer):
def setupPlt(x_label,y_label,title):
    # plt.gca().set_position([0.10, 0.15, 0.80, 0.77])
    plt.xlabel(x_label)
    # plt.title(title+"\n"+subtitle, fontsize=14)
    plt.title(title)
    plt.ylabel(y_label)
    # plt.annotate(footer, (0,0), (0, -40), xycoords='axes fraction', textcoords='offset points', va='top')

def saveAndClearPlt(plot_path):
    plt.savefig(plot_path)
    plt.clf()

if __name__ == "__main__":
    main()

