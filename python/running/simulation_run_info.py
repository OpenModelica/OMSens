class SimulationSpecs():
    def __init__(self, output_path, parameters_changed, model_name, executable_path):
        self.output_path = output_path
        self.parameters_changed = parameters_changed
        self.model_name = model_name
        self.executable = executable_path


class SweepSimulationSpecs(SimulationSpecs):
    def __init__(self, output_path, parameters_changed, model_name, executable_path, swept_params_info):
        super().__init__(output_path, parameters_changed, model_name, executable_path)
        self.swept_params_info = swept_params_info


class SweptParameterInfo():
    def __init__(self, name, default_val, new_val):
        self.name = name
        self.default_val = default_val
        self.new_val = new_val
