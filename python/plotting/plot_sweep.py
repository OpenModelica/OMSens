# Std
import os
import numpy
import pandas

# Mine
import matplotlib.pyplot as plt

class SweepPlot():
    def __init__(self, sweep_results):
        self.sweep_results = sweep_results
        self.swept_params_ids_mapping = idsForSweptParams(sweep_results)

    def plotInFolder(self, var_name, plots_folder_path, extra_ticks=[]):
        plot_path_without_extension = os.path.join(plots_folder_path, var_name)
        title, subtitle, footer = self.sweepingPlotTexts(self.sweep_results, var_name)
        footer_artist = setupPlot("Time", var_name, title, subtitle, footer)
        colors_iter = plotColorsForNumber(len(self.sweep_results.perturbed_runs))
        # Plot standard run that will be different than the other simulations results
        self.plotStandardRun(var_name)

        # Plot perturbed simulations from sweep
        for sweep_iter_results in self.sweep_results.perturbed_runs:
            simu_results = sweep_iter_results.simulation_results
            file_path = simu_results.output_path
            df_run = pandas.read_csv(file_path)
            label = self.labelForPerturbedRun(sweep_iter_results)
            color = next(colors_iter)
            plt.plot(df_run["time"], df_run[var_name], linewidth=1, linestyle='-', markersize=0, marker='o',
                     label=label, color=color)
        lgd = plt.legend(loc="center left", fontsize="small", fancybox=True, shadow=True,
                         bbox_to_anchor=(1, 0.5))
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
            p_perturb_perc_str = perturbationPercentageStringForParam(p_info)
            # Define the string for this param
            param_str = "({0})={1:.2f} [{2}]".format(p_id, p_info.new_val, p_perturb_perc_str)
            params_strs_list.append(param_str)
        # Join all the param strs to form the label for this run
        label = " | ".join(params_strs_list)
        return label

    def sweepingPlotTexts(self, sweep_specs, var_name):
        model_name = sweep_specs.model_name
        title = "Sweeping Plot for model: {model_name}".format(model_name=model_name)
        subtitle = "Plotting var: {var_name}".format(var_name=var_name)
        footer = self.footerFromSweepSpecs(sweep_specs)
        return (title, subtitle, footer)

    def footerFromSweepSpecs(self, sweep_specs):
        swept_params_str = self.sweptParamsStr(sweep_specs)
        fixed_params_str = fixedParamsStr(sweep_specs)
        footer = "{0}\n{1}".format(swept_params_str, fixed_params_str)
        return footer

    def sweptParamsStr(self, sweep_specs):
        swept_params_names = sweep_specs.swept_parameters_names
        params_with_id_list = ["{0} ({1})".format(p_name, self.swept_params_ids_mapping[p_name]) for p_name in
                               swept_params_names]
        joined_params_str = ", ".join(params_with_id_list)
        swept_params_info_str = "Swept parameters:  \n {0}".format(joined_params_str)
        return swept_params_info_str

    def plotStandardRun(self, var_name, color="black", label="STD_RUN", linestyle="-"):
        # Get simulation specs for std run
        std_run_specs = self.sweep_results.std_run
        # Read simulation results from disk
        df_simu = pandas.read_csv(std_run_specs.output_path)
        plt.plot(df_simu["time"], df_simu[var_name], linewidth=1, linestyle=linestyle, markersize=0, marker='o',
                 label=label, color=color)


def strSignForNumber(number):
    if number == 0:
        sign_str = ""
    if number < 0:
        sign_str = "-"
    if number > 0:
        sign_str = "+"
    return sign_str

def perturbationPercentageStringForParam(p_info):
    if p_info.default_val != 0:
        # If the divisor is not 0, calculate the percentage accordingly
        p_perturb_perc = ((p_info.new_val / p_info.default_val) - 1) * 100
        p_perturb_perc_sign_str = strSignForNumber(p_perturb_perc)
        p_perturb_perc_str = "{0}{1:.0f}%".format(p_perturb_perc_sign_str, abs(p_perturb_perc))
    else:
        # If the divisor is 0, there's nothing we can do. Just return a trivial string
        p_perturb_perc_str = "!"
    return p_perturb_perc_str

def idsForSweptParams(sweep_specs):
    # Get the parameters that were swept
    swept_params = sweep_specs.swept_parameters_names
    # Iterate swept parameters assigning each one a numerical id
    swept_params_ids_mapping = {swept_params[i]: i for i in range(len(swept_params))}
    return swept_params_ids_mapping


def plotColorsForNumber(n_colors):
    colors_list = plt.get_cmap('jet')(numpy.linspace(0, 1.0, n_colors))
    colors_iter = iter(colors_list)
    return colors_iter


def fixedParamsStr(sweep_specs):
    fixed_params_info = sweep_specs.fixed_parameters_info
    params_with_id_list = ["{0}={1}".format(p_info.name, p_info.new_val) for p_info in fixed_params_info]
    joined_params_str = ", ".join(params_with_id_list)
    swept_params_info_str = "Constant perturbed parameters:  \n {0}".format(joined_params_str)
    return swept_params_info_str


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
