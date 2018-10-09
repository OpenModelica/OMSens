class ModelOptimizationResult():
    def __init__(self, x0, x_opt, f_x0, f_x_opt, stop_time, variable_name):
        self.x0            = x0
        self.x_opt         = x_opt
        self.f_x0          = f_x0
        self.f_x_opt       = f_x_opt
        self.stop_time     = stop_time
        self.variable_name = variable_name
