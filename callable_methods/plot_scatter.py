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

logger = logging.getLogger("--Scatterplot Plotter--")
script_description = "Scatter plt"

# with open('/home/omsens/Documents/OMSens/callable_methods/test.txt', 'w+') as f:
#     f.write(filename_path)


def main():

    # with open('/home/omsens/Documents/OMSens/callable_methods/test.txt', 'w+') as f:
    #     f.write("halo")

    # 1. Get parameters for plot
    #  result filename path (where to go and fetch the PNG)
    #  input csv file
    #  t_{obs}: time of simulation for which the histogram will be made
    #  var    : variable for which the histogram will me made (for it's value on time t=t_{obs})
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

    filename_path = args.filename_path
    results_path = args.results_path
    time_value = args.time_value
    runs_path = results_path + "/" + "results/runs" + "/" + "perturbed/"

    variable = args.variable
    parameter = args.parameter

    if parameter is not None:
        plot_parameter(results_path, filename_path, runs_path, variable, parameter)
    elif variable is not None:
        plot_variable(filename_path, runs_path, variable)
    else:
        raise Exception('EXCEPTION')


def plot_parameter(results_path, filename_path, runs_path, variable, parameter):

    params_run = pd.read_csv(results_path + "/" + "results/parameters_run.csv", index_col=False)

    # TODO: analyze what to do with *_init in parameters saved.
    # TODO: generate groups: each value in x axis corresponds to a different value of 'parameter' in the runs
    #groups = params_run[['gamma', 'run_id']].groupby(by='gamma')#.agg(list).reset_index()
    # groups.to_csv('/home/omsens/Documents/results_experiments/test.csv')
    #groups.to_csv('/home/omsens/Documents/results_experiments/' + parameter + '.csv')

    params_run = params_run[params_run.run_id < 6]

    run_id_for_parameter = [int(x) for x in params_run['run_id'].tolist()]

    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    initial_vals = []
    final_vals = []
    run_ids = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            run_id = filename.split('/')[-1].replace('.csv', '').split('_')[1]
            if int(run_id) in run_id_for_parameter:
                z = pd.read_csv(runs_path + filename, index_col=False).dropna()

                # TODO: t_obs == t_final
                initial_val = float(z[variable].tolist()[0])
                initial_vals.append(initial_val)
                final_val = float(z[variable].tolist()[-1])
                final_vals.append(final_val)

                run_ids.append(run_id)

    # Generate scatter plot
    plt.title("Variable initial vs. final state (parameter = " + parameter + ")")
    plt.scatter(initial_vals, final_vals, c='b', alpha=0.5)
    for i, txt in enumerate(run_ids):
        plt.annotate(txt,
                     xy=(initial_vals[i], final_vals[i]),
                     fontsize=8)
    min_x_real = round(min(initial_vals), 3)
    max_x_real = round(max(initial_vals), 3)
    min_x = min_x_real - .05 * (max_x_real - min_x_real)
    max_x = max_x_real + .05 * (max_x_real - min_x_real)
    xticks = np.linspace(min_x, max_x, 10)
    plt.xticks(xticks)
    plt.xlim((min_x, max_x))
    plt.savefig(filename_path)


def plot_variable(filename_path, runs_path, variable):
    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    initial_vals = []
    final_vals   = []
    run_ids      = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            z = pd.read_csv(runs_path + filename, index_col=False).dropna()

            # TODO: t_obs == t_final
            initial_val = float(z[variable].tolist()[0])
            initial_vals.append(initial_val)
            final_val = float(z[variable].tolist()[-1])
            final_vals.append(final_val)

            run_id = filename.split('/')[-1].replace('.csv', '').split('_')[1]
            run_ids.append(run_id)

    # Generate scatter plot
    plt.title("Variable initial vs. final state (all runs)")
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
    plt.savefig(filename_path)


if __name__ == "__main__":
    main()
