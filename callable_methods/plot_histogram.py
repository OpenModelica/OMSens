import matplotlib
matplotlib.use('Agg')
import numpy as np

import matplotlib.pyplot as pl
import logging

logger = logging.getLogger("--Histogram Plotter--")
script_description = "Find parameters values that maximize or minimize a variable and plot the results"


def main():

    a = np.array([
        -0.86906864, -0.72122614, -0.18074998, -0.57190212, -0.25689268, -1., 0.68713553, 0.29597819, 0.45022949,
        0.37550592, 0.86906864, 0.17437203, 0.48704826, 0.2235648, 0.72122614, 0.14387731, 0.94194514
    ])

    fig = pl.hist(a, normed=0)
    pl.title('Mean')
    pl.xlabel("value")
    pl.ylabel("Frequency")
    pl.savefig("/home/omsens/Documents/results_experiments/plots/abc.png")


if __name__ == "__main__":
    main()
