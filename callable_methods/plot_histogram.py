import matplotlib
matplotlib.use('Agg')
import numpy as np
import os

import matplotlib.pyplot as plt
import logging
import argparse
import pandas as pd

logger = logging.getLogger("--Histogram Plotter--")
script_description = "Find parameters values that maximize or minimize a variable and plot the results"


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
                        help='Parameter for which to make histogram of values at specified time')
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

    vals = []
    for root, directory, files in os.walk(runs_path):
        for filename in files:
            z = pd.read_csv(runs_path + filename, index_col=False).dropna()
            vals.append(float(z[parameter].tolist()[-1]))
    df = pd.DataFrame({parameter: vals})
    vals = df[parameter].values

    # Set number of bins
    binwidth = 0.1
    bins = np.linspace(np.round(min(vals), 2), np.round(max(vals), 2), 1 / binwidth)
    # with open('/home/omsens/Documents/OMSens/callable_methods/zzz.txt', 'w+') as zzz:
    #     # zzz.write(str(bins))
    #     zzz.write(str(1/binwidth) + str(vals))

    # Generate histogram
    fig = plt.hist(vals, bins=bins)

    plt.title("Time: " + time_value + " & " + "Param: " + parameter)
    plt.xlabel(parameter)
    plt.ylabel("Frequency")
    plt.savefig(filename_path)


def set_bins(vals):
    mn = min(vals)
    mx = max(vals)
    if mx < 1:
        return [i for i in range(0, 1, 0.1)]
    return [i for i in range(0, round(mx, 1))]


if __name__ == "__main__":
    main()
