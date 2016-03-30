import logging #en reemplazo de los prints
logger = logging.getLogger("--CSV Plotter--") #un logger especifico para este modulo
import numpy as np
import matplotlib.pyplot as plt
def main():
    #ENTRADA:
    # csvs_list = ["BouncingBall_1_res.csv","BouncingBall_2_res.csv","BouncingBall_3_res.csv"]
    csvs_list = ["SystemDynamics.WorldDynamics.World3.Scenario_1_1_res.csv","SystemDynamics.WorldDynamics.World3.Scenario_1_2_res.csv"]
    plot_path = "tmp/plot.svg"
    var_name = "nr_resources"
    plot_title = "Ploteo de archivito"
    # /ENTRADA
    plotVarFromCSVs(var_name,csvs_list,plot_path, plot_title)
def plotVarFromCSVs(var_name,csvs_list,plot_path, plot_title):
    logger_plot_str = "Plotting:\n  plotvar:{var_name}\n  csvs:{csvs_list}\n path:{plot_path}".format(var_name=var_name,csvs_list=csvs_list,plot_path=plot_path)
    logger.debug(logger_plot_str)
    setupPlt("Time","f(x)",plot_title)

    for file_path in csvs_list:
        data = readFromCSV(file_path)
        file_name= file_path.split("/")[-1] #Creo que no funciona en MS-Win (barra distinta en paths)
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

