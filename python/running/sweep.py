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
        # Calculate the values per param
        self.values_per_param = valuesPerParamFromParamsInfos(self.perturbation_info_per_param)
        # Initialize builder
        self.model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)

    def runSweep(self, dest_folder_path):
        compiled_model = self.model_builder.buildToFolderPath(dest_folder_path)
        # Iterate combinations of parameters values

        # Create Sweep Results
        pass


# Aux
def valuesPerParamFromParamsInfos(perturbation_info_per_param):
    values_per_param = []
    for p_info in perturbation_info_per_param
        param_values = valuesForParameterFromParamInfo(p_info)
        values_per_param.append(param_values)
    return values_per_param


def valuesForParameterFromParamInfo(param_info):
    initial_value = param_info["initial_val"]
    delta = param_info["delta_percentage"]
    iterations = param_info["iterations"]
    lambda_i = lambda i: initial_value * (1 - (iterations / 2) * delta) + initial_value * delta * i
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
