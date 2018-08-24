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
    values_per_param = []
    for p_info in perturbation_info_per_param:
        perturbed_param_values = perturbedValuesForParams(p_info,params_defaults)
        values_per_param.append(perturbed_param_values)
    return values_per_param


def perturbedValuesForParams(param_info, params_defaults):
    # Disaggregate param info
    param_name = param_info["name"]
    delta      = param_info["delta_percentage"]
    iterations = param_info["iterations"]
    def_value  = params_defaults[param_name]
    # Calculate values for this param

    lambda_i = lambda i: def_value * (1 - (iterations / 2) * delta) + def_value * delta * i
    values = [lambda_i(i) for i in range(iterations)]
    param_values = \
        {
            "name": param_info["name"],
            "values": param_info["name"],
        }

class ParametersSweepResults():
    def __init__(self, model_name, swept_parameters, fixed_parameters, std_run, perturbed_runs):
        self.model_name = model_name
        self.swept_parameters_names = swept_parameters
        self.fixed_parameters_info = fixed_parameters
        self.std_run = std_run
        self.perturbed_runs = perturbed_runs
