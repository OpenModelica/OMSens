# Std
import os
import numpy
import pandas

# Mine
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class LinesPlotter():
    def __init__(self, plot_specs):
        self.plot_specs = plot_specs

    def plotInPath(self, plot_path):
        footer_artist = setupPlot(self.plot_specs.setup_specs)


def setupPlot(setup_specs):
    plt.style.use('fivethirtyeight')
    plt.gca().set_position([0.10, 0.15, 0.80, 0.77])
    plt.xlabel(setup_specs.x_label)
    plt.title(setup_specs.title + "\n" + setup_specs.subtitle, fontsize=14, y=1.08)
    plt.ylabel(setup_specs.y_label)
    plt.ticklabel_format(useOffset=False)  # So it doesn't use an offset on the x axis
    footer_artist = plt.annotate(setup_specs.footer, (1, 0), (0, -70), xycoords='axes fraction', textcoords='offset points',
                                 va='top', horizontalalignment='right')
    plt.margins(x=0.1, y=0.1)  # increase buffer so points falling on it are plotted
    return footer_artist

