# Std
import numpy
import itertools
# Mine
import modelica_interface.build_model as build_model


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
        params_vals_combinations = dict_product(self.values_per_param)

    def runSweep(self, dest_folder_path):
        # Create Sweep Results
        pass

    def valuesPerParam(self):
        return self.values_per_param

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
        pass
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
