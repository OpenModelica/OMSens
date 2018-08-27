# Std
import math
import numpy
# Mine
import modelica_interface.build_model as build_model


class ParametersSweeper():
    def __init__(self, model_name, model_file_path, start_time, stop_time, perturbation_info_per_param):
        # Save args
        self.model_name = model_name
        self.model_file_path = model_file_path
        self.start_time = start_time
        self.stop_time = stop_time
        self.perturbation_info_per_param = perturbation_info_per_param
        # Initialize builder
        self.model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)

    def runSweep(self, dest_folder_path):
        # Build model
        compiled_model = self.model_builder.buildToFolderPath(dest_folder_path)
        # Get the default values for the params to perturb using the compiled model
        params_defaults = self.defaultValuesForParamsToPerturb(compiled_model)

        # Calculate the values per param
        values_per_param = valuesPerParamFromParamsInfos(params_defaults,self.perturbation_info_per_param)
        # Iterate combinations of parameters values

        # Create Sweep Results
        pass


    # Instance auxs
    def _valuesPerParam(self, dest_folder_path):
        # For now this function is used only for testing
        # Build model
        compiled_model = self.model_builder.buildToFolderPath(dest_folder_path)
        # Get the default values for the params to perturb using the compiled model
        params_defaults = self.defaultValuesForParamsToPerturb(compiled_model)
        # Calculate the values per param
        values_per_param = valuesPerParamFromParamsInfos(params_defaults, self.perturbation_info_per_param)

        return values_per_param

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


class ParametersSweepResults():
    def __init__(self, model_name, swept_parameters, fixed_parameters, std_run, perturbed_runs):
        self.model_name = model_name
        self.swept_parameters_names = swept_parameters
        self.fixed_parameters_info = fixed_parameters
        self.std_run = std_run
        self.perturbed_runs = perturbed_runs
