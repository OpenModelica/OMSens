import matplotlib
matplotlib.use('Agg')
import numpy as np

import matplotlib.pyplot as plt
import logging
import argparse

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
    args = parser.parse_args()

    filename_path = args.filename_path

    a = np.array([
        -0.86906864, -0.72122614, -0.18074998, -0.57190212, -0.25689268, -1., 0.68713553, 0.29597819, 0.45022949,
        0.37550592, 0.86906864, 0.17437203, 0.48704826, 0.2235648, 0.72122614, 0.14387731, 0.94194514
    ])

    fig = plt.hist(a, normed=0)
    plt.title(filename_path)
    plt.xlabel("value")
    plt.ylabel("Frequency")
    plt.savefig(filename_path)


if __name__ == "__main__":
    main()
