import sys
sys.path.append('/home/omsens/Documents/OMSens/')

import matplotlib
matplotlib.use('Agg')
import os
import argparse
import pandas as pd
from plotting.scatter_plotter import ScatterPlotter

import logging
filehandler = logging.FileHandler("/home/omsens/Documents/results_experiments/logging/todo.log")
logger = logging.getLogger("plot_scatterplot")
logger.addHandler(filehandler)
logger.setLevel(logging.DEBUG)
logger.debug("Entra en plot_scatterplot")
script_description = "Scatter plot"


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

            # Lookup the parameter in parameters spanned: should find the run_id if there are no run_id's skipped
            parameter_val = groups[groups.run_id.apply(lambda xs: run_id in xs)][parameter].tolist()

            if len(parameter_val) > 0:

                logger.debug('FOUND: ' + str(run_id) + ' ' + str(parameter_val))
                parameter_val = parameter_val[0]

                # Aproximation of parameter value
                parameter_vals.append(parameter_val)

                # t_obs might be != t_final. Get last value of variable in simulation BEFORE t==time_value
                final_val = z[(z.time < float(time_value))][variable].values.tolist()[-1]

                variable_final_vals.append(final_val)
                run_ids.append(run_id)
            else:
                logger.warning('NOT FOUND: ' + str(run_id))

    # Generate scatter plot
    title = "RUNS (" + "Parameter:" + parameter + ")"
    title += " | "
    title += "Variable:" + variable + "(t=0)" + " vs. " + variable + "(t=" + str(time_value) + ") "
    ScatterPlotter.plot_parameter({
        'title': title,
        'filename_path': filename_path,
        'parameter_vals': parameter_vals,
        'variable_final_vals': variable_final_vals,
        'run_ids': run_ids,
        'parameter': parameter,
        'variable': variable
    })


def plot_variable(filename_path, runs_path, variable, time_value):
    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    initial_vals = []
    final_vals = []
    run_ids = []
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
    title = "ALL RUNS: " + variable + "(t=" + str(time_value) + ") "

    # TODO: Agregar parametros que fueron sweepeados en estas corridas !!!

    ScatterPlotter.plot_variable({
        'filename_path': filename_path,
        'title': title,
        'initial_vals': initial_vals,
        'final_vals': final_vals,
        'run_ids': run_ids,
        'variable': variable
    })


if __name__ == "__main__":
    main()
