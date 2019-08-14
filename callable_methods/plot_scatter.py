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

logger = logging.getLogger("--Scatterplot Plotter--")
script_description = "Scatter plt"


def main():
    args = parse_arguments()

    filename_path = args.filename_path
    results_path = args.results_path
    time_value = args.time_value
    runs_path = results_path + "/" + "results/runs" + "/" + "perturbed/"

    variable = args.variable
    parameter = args.parameter

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
                        metavar='results_paths',
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

    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    parameter_vals = []
    variable_final_vals = []
    run_ids = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            run_id = int(filename.split('/')[-1].replace('.csv', '').split('_')[1])

            z = pd.read_csv(runs_path + filename, index_col=False).dropna()

            parameter_val = groups[groups.run_id.apply(lambda xs: run_id in xs)][parameter].tolist()[0]
            # Aproximation of parameter value
            parameter_vals.append(parameter_val)

            # t_obs might be != t_final. Get last value of variable in simulation BEFORE t==time_value
            final_val = z[(z.time < float(time_value))][variable].values.tolist()[-1]

            variable_final_vals.append(final_val)
            run_ids.append(run_id)

    # Generate scatter plot
    title = "RUNS (" + "Parameter:" + parameter + ")"
    title += " | "
    title += "Variable:" + variable + "(t=0)" + " vs. " + variable + "(t=" + str(time_value) + ") "
    plt.title("\n".join(wrap(title, 40)))

    plt.scatter(parameter_vals, variable_final_vals, c='b', alpha=0.5)
    for i, run_id in enumerate(run_ids):
        plt.annotate(str(run_id),
                     xy=(parameter_vals[i], variable_final_vals[i]),
                     fontsize=8)
    min_x_real = round(min(parameter_vals), 3)
    max_x_real = round(max(parameter_vals), 3)
    min_x = min_x_real - .05 * (max_x_real - min_x_real)
    max_x = max_x_real + .05 * (max_x_real - min_x_real)
    xticks = np.linspace(min_x, max_x, 10)
    plt.xticks(xticks, rotation=30)
    plt.xlim((min_x, max_x))
    plt.xlabel(parameter)
    plt.ylabel(variable)

    # plt.tight_layout()
    plt.savefig(filename_path, figsize=(40, 40))


def plot_variable(filename_path, runs_path, variable, time_value):
    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    initial_vals = []
    final_vals   = []
    run_ids      = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            z = pd.read_csv(runs_path + filename, index_col=False).dropna()

            initial_val = float(z[variable].tolist()[0])
            initial_vals.append(initial_val)

            # t_obs might be != t_final. Get last value of variable in simulation BEFORE t==time_value
            final_val = z[(z.time < float(time_value))][variable].values.tolist()[-1]
            final_vals.append(final_val)

            run_id = filename.split('/')[-1].replace('.csv', '').split('_')[1]
            run_ids.append(run_id)

    # Generate scatter plot
    title = "ALL RUNS: " + variable + "(t=0)" + " vs. " + variable + "(t=" + str(time_value) + ") "
    plt.title("\n".join(wrap(title, 40)))

    plt.scatter(initial_vals, final_vals, c='b', alpha=0.5)
    for i, txt in enumerate(run_ids):
        plt.annotate(txt,
                     xy=(initial_vals[i], final_vals[i]),
                     fontsize=8)
    min_x_real = round(min(initial_vals), 3)
    max_x_real = round(max(initial_vals), 3)
    min_x = min_x_real - .05*(max_x_real-min_x_real)
    max_x = max_x_real + .05*(max_x_real-min_x_real)
    xticks = np.linspace(min_x, max_x, 10)
    plt.xticks(xticks)
    plt.xlim((min_x, max_x))
    plt.xlabel(variable)
    plt.ylabel(variable)

    plt.tight_layout()
    plt.savefig(filename_path)


if __name__ == "__main__":
    main()
