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

    # 1. Get parameters for plot
    #  result filename path (where to go and fetch the PNG)
    #  input csv file
    #  t_{obs}: time of simulation for which the histogram will be made
    #  var    : variable for which the histogram will me made (for it's value on time t=t_{obs})
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('--filename_path',
                        metavar='filename_path',
                        help='Filename path for output png file')
    parser.add_argument('--parameter',
                        metavar='parameter',
                        help='Parameter for which to make scatter of values at specified time on the different runs')
    parser.add_argument('--time_value',
                        metavar='time_value',
                        help='Specified time of simulation in which to measure value of specified parameter')
    parser.add_argument('--runs_path',
                        metavar='runs_path',
                        help='Results path directory (from where to get simulation results)')
    args = parser.parse_args()

    filename_path = args.filename_path
    parameter = args.parameter
    runs_path = args.runs_path + "/" + "perturbed/"
    time_value = args.time_value

    # Get data (1. get parameter initial value; 2. get parameter value at time t_obs)
    initial_vals = []
    final_vals   = []
    run_ids      = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            z = pd.read_csv(runs_path + filename, index_col=False).dropna()

            # TODO: t_obs == t_final
            initial_val = float(z[parameter].tolist()[0])
            initial_vals.append(initial_val)
            final_val = float(z[parameter].tolist()[-1])
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
