# Std
import logging  # instead of prints
# Project
import modelica_interface.build_model as build_model
import vectorial.optimization_result as optimization_result
import fortran_interface.curvif_simplified as curvi_mod
# Logging config
logger = logging.getLogger("ModelOptimizer")

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
        self.x0_dict  = {p:self.compiled_model.defaultParameterValue(p) for p in parameters_to_perturb}
        self.x0       = [self.x0_dict[p] for p in parameters_to_perturb]
        self.obj_func = createObjectiveFunctionForModel(self.compiled_model, parameters_to_perturb, target_var_name,
                                                        max_or_min)

    def optimize(self, percentage, epsilon):
        # Run a standard simulation to have f(x0) before optimizing
        f_x0 = self.compiled_model.quickSimulate(self.target_var_name)
        # Calculate bounds from percentage
        lower_bounds = [x*(1 - percentage/100) for x in self.x0]
        upper_bounds = [x*(1 + percentage/100) for x in self.x0]
        # Run the optimizer
        x_opt,f_opt_internal = curvi_mod.curvif_simplified(self.x0,self.obj_func,lower_bounds,upper_bounds,
                                                  epsilon)
        # Organize the parameters values in a dict
        x_opt_dict = {self.parameters_to_perturb[i]:x_opt[i] for i in range(len(self.parameters_to_perturb))}
        # If we were maximizing, we have to multiply again by -1
        if self.max_or_min == "max":
            f_opt = -f_opt_internal
        else:
            # If we were minimizing, the internal f(x) will be the final one
            f_opt = f_opt_internal
        # Initialize optimization result object
        optim_result = optimization_result.ModelOptimizationResult(self.x0_dict, x_opt_dict, f_x0, f_opt, self.stop_time,
                                                                   self.target_var_name)
        # Return optimization result
        return optim_result

# Auxs
def createObjectiveFunctionForModel(compiled_model, param_names, target_var_name, max_or_min):
    # We initialize a function with "dynamic hardcoded variables". It will have this variables fixed with the value
    #  from execution context of the function that defined it
    def objectiveFunction(params_vals):
        # Organize param vals
        params_vals_dict = {p_name:p_val for p_name,p_val in zip(param_names, params_vals)}
        # Run a quick simulation
        var_val = compiled_model.quickSimulate(target_var_name, params_vals_dict)
        # Log simu result
        x_str = ", ".join([str(x) for x in params_vals])
        logging_str = "\n   x: {1}\n   f(x) = {0}".format(var_val, x_str)
        logger.info(logging_str)
        # Assign a sign depending if maximizing or minimizing
        if max_or_min == "max":
            obj_func_val = -var_val
        elif max_or_min == "min":
            obj_func_val = var_val
        return obj_func_val

    return objectiveFunction
