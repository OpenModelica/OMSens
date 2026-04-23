from typing import Any

class SimulationResults():
    def __init__(self, output_path: Any, model_name: str, executable_path:str, std_output:str):
        self.output_path = output_path
        self.model_name = model_name
        self.executable = executable_path
        self.std_output = std_output


class PerturbedParameterInfo():
    def __init__(self, name, default_val, new_val):
        self.name = name
        self.default_val = default_val
        self.new_val = new_val
