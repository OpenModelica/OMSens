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
from textwrap import wrap

logger = logging.getLogger("--Histogram Plotter--")
script_description = "Hst plotter"


def main():
    args = parse_arguments()

    filename_path = args.filename_path
    results_path = args.results_path
    time_value = args.time_value
    runs_path = results_path + "/" + "results/runs" + "/" + "perturbed/"

    parameter = args.parameter
    variable = args.variable

    if parameter is not None:
        plot_parameter(results_path, filename_path, runs_path, variable, parameter, time_value)
    elif variable is not None:
        plot_variable(filename_path, runs_path, variable, time_value)
    else:
        raise Exception('EXCEPTION')


def parse_arguments():
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
    return args


def plot_parameter(results_path, filename_path, runs_path, variable, parameter, time_value):

    params_run = pd.read_csv(results_path + "/" + "results/parameters_run.csv", index_col=False)
    groups = params_run[[parameter, 'run_id']].groupby(by=parameter)['run_id'].apply(list).reset_index()

    n_groups = len(groups[parameter].unique().tolist())
    dim = 1
    for i in [4, 3, 2, 1]:
        if i**2 >= n_groups:
            dim = i
    n_rows = dim
    n_cols = dim

    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    param_final_values = {}
    fig = plt.figure()
    for i, row in groups.iterrows():
        param_value = row[parameter]
        param_final_values[param_value] = []
        runs_ids = row['run_id']
        for run_id in runs_ids:
            z = pd.read_csv(runs_path + '/run_' + str(run_id) + '.csv', index_col=False).dropna()
            # t_obs might be != t_final. Get last value of variable in simulation BEFORE t==time_value
            final_val = z[(z.time < float(time_value))][variable].values.tolist()[-1]
            param_final_values[param_value].append(final_val)

        ax = fig.add_subplot(n_rows, n_cols, i+1)
        ax.hist(param_final_values[param_value])
        ax.set_title(parameter + ": " + str(round(param_value, 3)))

        ax.set_xlabel(variable)

    fig.suptitle("t = " + str(time_value), fontsize=16)

    fig.tight_layout()
    # fig.subplots_adjust(top=30)

    plt.savefig(filename_path)


def plot_variable(filename_path, runs_path, variable, time_value):

    vals = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            z = pd.read_csv(runs_path + filename, index_col=False).dropna()

            # t_obs might be != t_final. Get last value of variable in simulation BEFORE t==time_value
            val = z[(z.time < float(time_value))][variable].values.tolist()[-1]

            vals.append(val)
    df = pd.DataFrame({variable: vals})
    vals = df[variable].values

    # Set number of bins
    binwidth = 0.1
    bins = np.linspace(np.round(min(vals), 2), np.round(max(vals), 2), 1 / binwidth)

    # Generate histogram
    fig = plt.hist(vals, bins=bins)

    # TODO: Definir si agregar o no parametros que fueron sweepeados en estas corridas !!!

    title = "Variable:" + variable + "(t=" + str(time_value) + ") "
    plt.title("\n".join(wrap(title, 40)))
    plt.xlabel(variable)
    plt.ylabel("Number of runs")
    plt.savefig(filename_path)


if __name__ == "__main__":
    main()
