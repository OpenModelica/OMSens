# Std
import os
import numpy
import pandas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Project
import plotting.plot_lines as plot_lines
import plotting.plot_specs as plot_specs

class VectorialPlotter():
    def __init__(self, optim_result):
        # Save args
        self.optim_result = optim_result
