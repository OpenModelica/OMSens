class ParametersSweepSpecs():
    def __init__(self, model_name, swept_parameters, fixed_parameters, std_run, perturbed_runs):
        self.model_name = model_name
        self.swept_parameters = swept_parameters
        self.fixed_parameters = fixed_parameters
        self.std_run = std_run
        self.perturbed_runs = perturbed_runs
