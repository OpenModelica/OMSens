import modelica_interface.build_model as build_model
import fortran_interface.curvif_simplified as curvi_mod

class ModelOptimizer():
    def __init__(self, model_name, start_time, stop_time, model_file_path, target_var_name,
                 parameters_to_perturb, max_or_min, build_folder_path):
        # Save args
        self.model_name            = model_name
        self.start_time            = start_time
        self.stop_time             = stop_time
        self.model_file_path       = model_file_path
        self.target_var_name       = target_var_name
        self.parameters_to_perturb = parameters_to_perturb
        self.max_or_min            = max_or_min
        # Define members from args
        # Initialize builder
        model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)
        # Build model
        self.compiled_model = model_builder.buildToFolderPath(build_folder_path)
        self.x0       = [self.compiled_model.defaultParameterValue(p) for p in parameters_to_perturb]
        self.obj_func = createObjectiveFunctionForModel(self.compiled_model, parameters_to_perturb, target_var_name,
                                                        max_or_min)
    def optimize(self, percentage, epsilon):
        # Calculate bounds from percentage
        lower_bounds = [x*(1 - percentage/100) for x in self.x0]
        upper_bounds = [x*(1 + percentage/100) for x in self.x0]
        # Run the optimizer
        x_opt,f_opt_internal = curvi_mod.curvif_simplified(self.x0,self.obj_func,lower_bounds,upper_bounds,
                                                  epsilon)
        # Restore defaults of the values changed by curvi
        self.compiled_model.restoreAllParametersToDefaultValues()
        # Organize the parameters values in a dict
        x_opt_dict = {self.parameters_to_perturb[i]:x_opt[i] for i in range(len(self.parameters_to_perturb))}
        # If we were maximizing, we have to multiply again by -1
        if self.max_or_min == "max":
            f_opt = -f_opt_internal
        else:
            # If we were minimizing, the internal f(x) will be the final one
            f_opt = f_opt_internal
        return x_opt_dict, f_opt

# Auxs
def createObjectiveFunctionForModel(compiled_model, param_names, target_var_name, max_or_min):
    # We initialize a function with "dynamic hardcoded variables". It will have this variables fixed with the value
    #  from execution context of the function that defined it
    def objectiveFunction(params_vals):
        # Set the values for each respective parameter
        for i in range(len(param_names)):
            p_name = param_names[i]
            p_val = params_vals[i]
            compiled_model.setParameterStartValue(p_name, p_val)
        # Run the simulation
        var_val = compiled_model.quickSimulate(target_var_name)
        # Assign a sign depending if maximizing or minimizing
        if max_or_min == "max":
            obj_func_val = -var_val
        elif max_or_min == "min":
            obj_func_val = var_val
        return obj_func_val

    return objectiveFunction
