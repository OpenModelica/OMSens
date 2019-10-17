import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap


class ScatterPlotter:

    @classmethod
    def plot_parameter(cls, params):
        filename_path = params['filename_path']
        title = params['title']
        parameter_vals = params['parameter_vals']
        variable_final_vals = params['variable_final_vals']
        run_ids = params['run_ids']
        parameter = params['parameter']
        variable = params['variable']

        min_x_real = round(min(parameter_vals), 3)
        max_x_real = round(max(parameter_vals), 3)
        min_x = min_x_real - .05 * (max_x_real - min_x_real)
        max_x = max_x_real + .05 * (max_x_real - min_x_real)

        if min_x == max_x:
            unique_val = parameter_vals[0]
            min_x = unique_val - 0.5 * unique_val
            max_x = unique_val + 0.5 * unique_val

        min_y_real = round(min(variable_final_vals), 3)
        max_y_real = round(max(variable_final_vals), 3)

        len_x_axis = np.abs(max_x - min_x)
        len_y_axis = np.abs(max_y_real - min_y_real)

        arrow_factor = 0.05

        for i, run_id in enumerate(run_ids):
            plt.annotate('run_id='+str(run_id),
                         arrowprops=dict(
                             facecolor='black',
                             width=0.8, headwidth=8,
                             headlength=6,
                             shrink=0.05
                         ),
                         xy=(parameter_vals[i], variable_final_vals[i]),
                         xytext=(parameter_vals[i] + arrow_factor * len_x_axis, variable_final_vals[i] + arrow_factor * len_y_axis),
                         fontsize=8)

        xticks = np.linspace(min_x, max_x, 10)

        plt.title("\n".join(wrap(title, 40)))
        plt.scatter(parameter_vals, variable_final_vals, c='b', alpha=0.5)
        plt.xticks(xticks, rotation=30)
        plt.xlim((min_x, max_x))
        plt.xlabel(parameter)
        plt.ylabel(variable)

        # Set rectangle width space so that the arrows are visible
        plt.tight_layout(rect=[0, 0, 0.95, 0.95])

        plt.savefig(filename_path, figsize=(50, 50))

    @classmethod
    def plot_variable(cls, params):

        filename_path = params['filename_path']
        title = params['title']
        initial_vals = params['initial_vals']
        final_vals = params['final_vals']
        run_ids = params['run_ids']
        variable = params['variable']

        min_x_real = round(min(initial_vals), 3)
        max_x_real = round(max(initial_vals), 3)
        min_x = min_x_real - .05 * (max_x_real - min_x_real)
        max_x = max_x_real + .05 * (max_x_real - min_x_real)

        if min_x == max_x:
            unique_val = initial_vals[0]
            min_x = unique_val - 0.5 * unique_val
            max_x = unique_val + 0.5 * unique_val

        min_y_real = round(min(final_vals), 3)
        max_y_real = round(max(final_vals), 3)

        len_x_axis = np.abs(max_x - min_x)
        len_y_axis = np.abs(max_y_real - min_y_real)

        arrow_factor = 0.05

        for i, txt in enumerate(run_ids):
            plt.annotate('rund_id=' + txt,
                         arrowprops=dict(
                             facecolor='black',
                             width=0.8, headwidth=8,
                             headlength=6,
                             shrink=0.05
                         ),
                         xy=(initial_vals[i], final_vals[i]),
                         xytext=(initial_vals[i] + arrow_factor * len_x_axis,
                                 final_vals[i] + arrow_factor * len_y_axis),
                         fontsize=8)

        xticks = np.linspace(min_x, max_x, 10)

        # Generate plot
        plt.title("\n".join(wrap(title, 40)))
        plt.scatter(initial_vals, final_vals, c='b', alpha=0.5)

        plt.xticks(xticks)
        plt.xlim((min_x, max_x))
        plt.xlabel(variable)
        plt.ylabel(variable)

        plt.tight_layout()
        plt.savefig(filename_path)
