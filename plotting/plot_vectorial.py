# Std
import os
import numpy
import pandas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Project
import plotting.plot_lines as plot_lines
import plotting.plot_specs as plot_specs

class VectorialPlotter():
    def __init__(self, optim_result, df_x0_run, df_x_opt_run):
        # Save args
        self.optim_result = optim_result
        self.df_x0_run    = df_x0_run
        self.df_x_opt_run = df_x_opt_run

    def plotInFolder(self, plots_folder_path, extra_ticks=[]):
        # Define plot file name base
        file_name_without_extension = self.optim_result.variable_name
        plot_path_without_extension = os.path.join(plots_folder_path, file_name_without_extension)
        # Define setup specs
        setup_specs = self.plotSetupSpecs(extra_ticks)
        # Define std run specs
        std_run_specs = self.standardRunLineSpecs()
        # Define perturbed run specs
        perturbed_run_specs = self.perturbedRunSpecs()
        # Initialize plot_specs
        lines_specs = [std_run_specs, perturbed_run_specs]
        vect_plot_specs = plot_specs.PlotSpecs(setup_specs, lines_specs)
        # Initialize lines plotter
        lines_plotter = plot_lines.LinesPlotter(vect_plot_specs)
        # Plot
        lines_plotter.plotInPath(plot_path_without_extension)
        # Return only the .png plot path for now
        png_plot_path = "{0}.png".format(plot_path_without_extension)
        return png_plot_path

    def perturbedRunSpecs(self):
        # Prepare info
        df         = self.df_x_opt_run
        x_var      = "time"
        y_var      = self.optim_result.variable_name
        linewidth  = 1
        linestyle  = "-"
        markersize = 0
        marker     = 'o'
        label      = "optimum"
        color      = "red"
        # Initialize plot line specs
        std_run_specs = plot_specs.PlotLineSpecs(
            df         = df,
            x_var      = x_var,
            y_var      = y_var,
            linewidth  = linewidth,
            linestyle  = linestyle,
            markersize = markersize,
            marker     = marker,
            label      = label,
            color      = color
        )
        return std_run_specs

    def standardRunLineSpecs(self):
        # Prepare info
        df         = self.df_x0_run
        x_var      = "time"
        y_var      = self.optim_result.variable_name
        linewidth  = 1
        linestyle  = "-"
        markersize = 0
        marker     = 'o'
        label      = "STD_RUN"
        color      = "black"
        # Initialize plot line specs
        std_run_specs = plot_specs.PlotLineSpecs(
           df         = df,
           x_var      = x_var,
           y_var      = y_var,
           linewidth  = linewidth,
           linestyle  = linestyle,
           markersize = markersize,
           marker     = marker,
           label      = label,
           color      = color
        )
        return std_run_specs

    def plotSetupSpecs(self, extra_ticks):
        # Get the info for the plot setup specs
        title, subtitle, footer = ("","","") # empty for now
        x_label = self.optim_result.variable_name
        y_label = "Time"
        # Initialize the plot setup specs
        setup_specs = plot_specs.PlotSetupSpecs(
            title       = title,
            subtitle    = subtitle,
            footer      = footer,
            x_label     = x_label,
            y_label     = y_label ,
            extra_ticks = extra_ticks
        )
        return setup_specs
