# Std
import numpy
import itertools
import os
# Mine
import modelica_interface.build_model as build_model
import filesystem.files_aux as files_aux
import running.simulation_run_info as simu_run_info


class ParametersSweeper():
    def __init__(self, model_name, model_file_path, start_time, stop_time, perturbation_info_per_param,
                 build_folder_path):
        # Save args
        self.model_name = model_name
        self.model_file_path = model_file_path
        self.start_time = start_time
        self.stop_time = stop_time
        self.perturbation_info_per_param = perturbation_info_per_param
        # Initialize builder
        self.model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)
        # Build model
        self.compiled_model = self.model_builder.buildToFolderPath(build_folder_path)
        # Get the default values for the params to perturb using the compiled model
        self.params_defaults = self.defaultValuesForParamsToPerturb(self.compiled_model)
        # Calculate the values per param
        self.values_per_param = valuesPerParamFromParamsInfos(self.params_defaults, self.perturbation_info_per_param)
        # Generate all possible combinations
        self.params_vals_combinations = dict_product(self.values_per_param)

    def runSweep(self, dest_folder_path):
        # Make folder for runs
        runs_folder_name = "runs"
        runs_folder_path = os.path.join(dest_folder_path, runs_folder_name)
        files_aux.makeFolderWithPath(runs_folder_path)
        # Run STD run
        std_run_name = "std_run.csv"
        std_run_path = os.path.join(runs_folder_path, std_run_name)
        std_run_results = self.compiled_model.simulate(std_run_path)
        # Make dir for perturbed runs
        perturbed_runs_folder_name = "runs"
        perturbed_runs_folder_path = os.path.join(dest_folder_path, perturbed_runs_folder_name)
        files_aux.makeFolderWithPath(perturbed_runs_folder_path)
        # Run the different values combinations
        sweep_iterations = []
        for i in range(len(list(self.params_vals_combinations))):
            vals_comb = self.params_vals_combinations[i]
            # Perturb the parameters for this iteration
            swept_params_info = []
            for param_name in vals_comb:
                # Instantiate perturbed params infos
                param_default_val = self.params_defaults[param_name]
                param_perturbed_val = vals_comb[param_name]
                perturbed_param_info = simu_run_info.PerturbedParameterInfo(param_name, param_default_val,
                                                                            param_perturbed_val)
                # Save the perturbed param info
                swept_params_info.append(perturbed_param_info)
                # Change the value in the model
                self.compiled_model.setParameterStartValue(param_name, vals_comb[param_name])
            # Run the simulation
            simu_csv_name = "run_{0}.csv".format(i)
            simu_csv_path = os.path.join(perturbed_runs_folder_path, simu_csv_name)
            simu_results = self.compiled_model.simulate(simu_csv_path)
            # Instantiate sweep iteration results
            sweep_iter_results = SweepIterationResults(simu_results, swept_params_info)
            # Add results to list
            sweep_iterations.append(sweep_iter_results)
        # Instantiate sweep results
        swept_params_names = [x["name"] for x in self.perturbation_info_per_param]
        fixed_params = []
        sweep_results = ParametersSweepResults(self.model_name, swept_params_names, fixed_params, std_run_results,
                                               sweep_iterations, )
        return sweep_results

    def valuesPerParameter(self):
        return self.values_per_param

    def parametersValuesCombinations(self):
        return self.params_vals_combinations

    # Auxs
    def defaultValuesForParamsToPerturb(self,compiled_model):
        # Get list of params to perturb
        params_to_perturb = [ x["name"] for x in self.perturbation_info_per_param ]
        # Using the compiled model, ask for the default value of each one
        params_defaults = {}
        for p in params_to_perturb:
            p_def_val = compiled_model.defaultParameterValue(p)
            params_defaults[p] = p_def_val
        return params_defaults




# Aux
def valuesPerParamFromParamsInfos(params_defaults, perturbation_info_per_param):
    values_per_param = {}
    for p_info in perturbation_info_per_param:
        # Disaggregate param info
        param_name = p_info["name"]
        delta = p_info["delta_percentage"]
        iterations = p_info["iterations"]
        def_value = params_defaults[param_name]
        param_values = valuesForDeltaItersAndDefaultVal(delta, iterations, def_value)
        values_per_param[param_name] = param_values
    return values_per_param


def valuesForDeltaItersAndDefaultVal(delta_percentage, iterations, def_value):
    # Get limits
    left_limit = def_value * (1 - delta_percentage / 100)
    right_limit = def_value * (1 + delta_percentage / 100)
    # Organize different cases for #iters
    if iterations == 1:
        # If 1 iteration, then include only the default value
        values = [def_value]
    elif iterations <= 0:
        # If 0 or less iterations, this should fail
        raise Exception("The #iterations should be >= 1")
    else:
        # 2 or more iterations, use numpys linspace
        values = numpy.linspace(left_limit, right_limit, iterations)
    return values


def dict_product(dict_of_lists):
    return (dict(zip(dict_of_lists, x)) for x in itertools.product(*dict_of_lists.values()))


class ParametersSweepResults():
    def __init__(self, model_name, swept_parameters, fixed_parameters, std_run, perturbed_runs):
        self.model_name = model_name
        self.swept_parameters_names = swept_parameters
        self.fixed_parameters_info = fixed_parameters
        self.std_run = std_run
        self.perturbed_runs = perturbed_runs


class SweepIterationResults():
    def __init__(self, simulation_results, swept_params_info):
        self.simulation_results = simulation_results
        self.swept_params_info = swept_params_info
