import sys
sys.path.append('/home/omsens/Documents/OMSens/')

import matplotlib
matplotlib.use('Agg')
import numpy as np
import os

import matplotlib.pyplot as plt
import logging
import argparse
import pandas as pd

logger = logging.getLogger("--Histogram Plotter--")
script_description = "Hst plotter"


def main():

    # 1. Get parameters for plot
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('--filename_path',
                        metavar='filename_path',
                        help='Filename path for output png file')
    parser.add_argument('--time_value',
                        metavar='time_value',
                        help='Specified time of simulation in which to measure value of specified parameter')
    parser.add_argument('--results_path',
                        metavar='results_path',
                        help='Results path directory (from where to get simulation results)')
    parser.add_argument('--variable',
                        metavar='variable',
                        help='Variable for which to make scatter of values at specified time on the different runs')
    parser.add_argument('--parameter',
                        metavar='parameter',
                        help='Parameter for which to make scatter of values at specified time on the different runs')
    args = parser.parse_args()

    filename_path = args.filename_path
    results_path = args.results_path
    time_value = args.time_value
    runs_path = results_path + "/" + "results/runs" + "/" + "perturbed/"

    parameter = args.parameter
    variable = args.variable

    if parameter is not None:
        # plot_parameter(results_path, filename_path, runs_path, variable, parameter)
        plot_variable(filename_path, runs_path, variable, time_value)
    elif variable is not None:
        plot_variable(filename_path, runs_path, variable, time_value)
    else:
        raise Exception('EXCEPTION')

def plot_parameter():
    pass


def plot_variable(filename_path, runs_path, variable, time_value):
    vals = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            z = pd.read_csv(runs_path + filename, index_col=False).dropna()

            # TODO: t_obs == t_final
            vals.append(float(z[variable].tolist()[-1]))
    df = pd.DataFrame({variable: vals})
    vals = df[variable].values

    # Set number of bins
    binwidth = 0.1
    bins = np.linspace(np.round(min(vals), 2), np.round(max(vals), 2), 1 / binwidth)

    # Generate histogram
    fig = plt.hist(vals, bins=bins)

    plt.title("Time: " + time_value + " & " + "Param: " + variable)
    plt.xlabel(variable)
    plt.ylabel("Frequency")
    plt.savefig(filename_path)


if __name__ == "__main__":
    main()
