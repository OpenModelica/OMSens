# Reqs
- Python 3 with some extra libraries. (anaconda3 includes all the dependencies)
- Linux (hasn't been tested on Windows yet)
# How to:
## Run:
To run a predefined parameter sweep experiment, modify global variables at the top of in world3\_scenarios\_sweeps.py and then run the following command:

    python world3_scenarios_sweeps.py
If errors occur, it's likely because of a missing python module. Install the python module specified in the error message and try again (anaconda3 might eliminate these problems).
## Interpret results:
If the script is run in %dir%, then this script will create an output folder with
path

    %dir$/tmp/modelica_outputs/<date>/<time>/
 
There, if running the world3 predefined sweeps (i.e. those offered as inline examples in world3\_scenarios\_sweeps.py), it will create a new folder scenario\_<i> for each scenario ran, and inside those folders:

  - A .mos script that loads the Modelica Model, sets the fixed initial
parameter (if any) and runs the sweep for the desired sweep_variable(s)
  - The resulting csv output files. One for each iteration of the sweep.
  - omc_log.txt: output of the .mos script
  - run_info.txt: settings of the .py script (sweep_variables,
    iterations, etc). These are the values used in the .mos script and for
    plotting the results.
  - out_of_range_cases.txt: This file is generated when the interpolation
function from SystemDynamics model in OpenModelica is asked to
interpolate values outside the default range (lower than the minimum or greater
than the maximum). In those cases, we extrapolate linearly outwards the standard interval.
  - plots/<var>.svg: the plot for the plot_variable (different than the
sweep_variables) for each of its values for each iteration.
