# Std
import os
import numpy
import pandas

# Mine
import matplotlib.pyplot as plt

class SweepPlot():
    def __init__(self, sweep_specs):
        self.sweep_specs = sweep_specs
        self.swept_params_ids_mapping = idsForSweptParams(sweep_specs)

    def plotInFolder(self, var_name, plots_folder_path, extra_ticks=[]):
        plot_path_without_extension = os.path.join(plots_folder_path, var_name)
        title, subtitle, footer = sweepingPlotTexts(self.sweep_specs, var_name)
        footer_artist = setupPlot("Time", var_name, title, subtitle, footer)
        colors_iter = plotColorsForNumber(len(self.sweep_specs.perturbed_runs))
        # Plot standard run that will be different than the other simulations results
        self.plotStandardRun(var_name)

        # Plot perturbed simulations from sweep
        for perturbed_run in self.sweep_specs.perturbed_runs:
            file_path = perturbed_run.output_path
            df_run = pandas.read_csv(file_path)
            label = self.labelForPerturbedRun(perturbed_run)
            color = next(colors_iter)
            plt.plot(df_run["time"], df_run[var_name], linewidth=1, linestyle='-', markersize=0, marker='o',
                     label=label, color=color)
        lgd = plt.legend(loc="center left", fontsize="small", fancybox=True, shadow=True,
                         bbox_to_anchor=(1, 0.5))  # A la derecha
        # lgd = plt.legend(loc="center left",fontsize="small",fancybox=True, shadow=True, bbox_to_anchor=(0.5,-0.5)) #Abajo (anda mal)
        setupXTicks(extra_ticks)
        saveAndClearPlt(plot_path_without_extension, lgd, footer_artist)

    def labelForPerturbedRun(self, sweep_simu_specs):
        # Get the info for each swept param (and not also fixed perturbed param)
        swept_params_info = sweep_simu_specs.swept_params_info
        # Iterate the perturbed parameters infos
        params_strs_list = []
        for p_info in swept_params_info:
            # Get the name of the param
            p_name = p_info.name
            # Get the ID for that name
            p_id = self.swept_params_ids_mapping[p_name]
            # Get the new val and the perturbation percentage from the default val
            p_perturb_perc = (p_info.default_val / p_info.new_val) * 100
            # Define the string for this param
            param_str = "{0}={1:.2f} [{2}]".format(p_id, p_info.new_val, p_perturb_perc)
            params_strs_list.append(param_str)
        # Join all the param strs to form the label for this run
        label = " | ".join(params_strs_list)
        return label

    def plotStandardRun(self, var_name, color="black", label="STD_RUN", linestyle="-"):
        # Get simulation specs for std run
        std_run_specs = self.sweep_specs.std_run
        # Read simulation results from disk
        df_simu = pandas.read_csv(std_run_specs.output_path)
        plt.plot(df_simu["time"], df_simu[var_name], linewidth=1, linestyle=linestyle, markersize=0, marker='o',
                 label=label, color=color)


def idsForSweptParams(sweep_specs):
    # Get the parameters that were swept
    swept_params = sweep_specs.swept_parameters
    # Iterate swept parameters assigning each one a numerical id
    swept_params_ids_mapping = {swept_params[i]: i for i in range(len(swept_params))}
    return swept_params_ids_mapping


def plotColorsForNumber(n_colors):
    colors_list = plt.get_cmap('jet')(numpy.linspace(0, 1.0, n_colors))
    colors_iter = iter(colors_list)
    return colors_iter


def sweptParamsStr(sweep_specs):
    swept_params = sweep_specs.swept_parameters
    params_with_id_list = ["{0} ({1})".format(swept_params[i], i) for i in range(0, len(swept_params))]
    joined_params_str = ", ".join(params_with_id_list)
    swept_params_info_str = "Swept parameters:  \n {0}".format(joined_params_str)
    return swept_params_info_str


def fixedParamsStr(sweep_specs):
    len_fixed_params = len(sweep_specs.fixed_parameters)
    fixed_params_str = "Alongside the swept parameters," \
                       " {0} parameters were perturbed with a fixed value in all iterations".format(len_fixed_params)
    return fixed_params_str


def sweepingPlotTexts(sweep_specs, var_name):
    model_name = sweep_specs.model_name
    title = "Sweeping Plot for model: {model_name}".format(model_name=model_name)
    subtitle = "Plotting var: {var_name}".format(var_name=var_name)
    footer = footerFromSweepSpecs(sweep_specs)
    return (title, subtitle, footer)


def footerFromSweepSpecs(sweep_specs):
    swept_params_str = sweptParamsStr(sweep_specs)
    fixed_params_str = fixedParamsStr(sweep_specs)
    footer = "{0}\n{1}".format(swept_params_str, fixed_params_str)
    return footer


def setupPlot(x_label, y_label, title, subtitle, footer):
    plt.style.use('fivethirtyeight')
    plt.gca().set_position([0.10, 0.15, 0.80, 0.77])
    plt.xlabel(x_label)
    plt.title(title + "\n" + subtitle, fontsize=14, y=1.08)
    plt.ylabel(y_label)
    plt.ticklabel_format(useOffset=False)  # So it doesn't use an offset on the x axis
    footer_artist = plt.annotate(footer, (1, 0), (0, -70), xycoords='axes fraction', textcoords='offset points',
                                 va='top', horizontalalignment='right')
    plt.margins(x=0.1, y=0.1)  # increase buffer so points falling on it are plotted
    return footer_artist


def setupXTicks(extra_ticks):
    # Get the ticks automatically generated by matplotlib
    auto_x_ticks = list(plt.xticks()[0])
    # Trim the borders (excessively large)
    auto_x_ticks_wo_borders = auto_x_ticks[1:-1]
    x_ticks = sorted(auto_x_ticks_wo_borders + extra_ticks)
    plt.xticks(x_ticks, rotation='vertical')  # add extra ticks (1975 for vermeulen for example)


def saveAndClearPlt(plot_path_without_extension, lgd, footer_artist, extra_lgd=None):
    extensions = [".svg", ".png"]
    for ext in extensions:
        plot_path = plot_path_without_extension + ext
        if extra_lgd:
            # If two legends (for when the plot has variables with different scale)
            plt.savefig(plot_path, bbox_extra_artists=(lgd, extra_lgd, footer_artist), bbox_inches='tight')
        else:
            # If only one legend
            plt.savefig(plot_path, bbox_extra_artists=(lgd, footer_artist), bbox_inches='tight')
    plt.clf()
