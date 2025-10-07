# This class models the settings respective to a parameter in the context of a sweep.
#  We use it to ease the customization of runs. The user only needs to know the parameter name, the formula to use and the # of iterations

# Std
from abc import ABC, abstractmethod    # to define abstract clasess and methods
#Mine:
import world3_specific.standard_run_params_defaults

class ParameterSweepSettings(ABC):
    pass

class OrigParameterSweepSettings(ParameterSweepSettings):
    def __init__(self,param_name, sweeping_formula, iterations):
        # Initialize from input
        self.param_name       = param_name
        self.iterations       = iterations
        # Calculate rest of internal variables:
        ## Get parameter default value from database
        self.default_value = defaultValueForParam(self.param_name)
        self._sweeping_formula = sweeping_formula
    def formula(self,i_var_name):
        formula_str = formulaStrFromSweepingFormula(self._sweeping_formula,self,i_var_name)
        return formula_str
    def __str__(self):
        return "(param_name " + str(self.param_name) + ",iterations " + str(self.iterations) + ",default_value " + str(self.default_value) + ",sweeping_formula " + str(self._sweeping_formula) + ")"
    def __repr__(self):
        return "(param_name " + str(self.param_name) + ",iterations " + str(self.iterations) + ",default_value " + str(self.default_value) + ",sweeping_formula " + str(self._sweeping_formula) + ")"

class CustomParameterSweepSettings(ParameterSweepSettings):
#### This class is in production  ####
# This class defines settings for a "custom parameter". That is, a parameter added by hand instead of the originals.
#   The objects in this class need to be set manually their default parameter (as we can't fetch it from the database)
    pass


### AUX:
# 
def defaultValueForParam(param_name):
    params_info_list = world3_specific.standard_run_params_defaults.w3_params_info_list
    for def_param_name,def_param_val,def_param_desc in params_info_list:
        if param_name == def_param_name:
            return def_param_val
    # If the parameter was not found, raise exception
    raise ParameterNotFoundException("The parameter "+ param_name +" was not found among the defaults")
def formulaStrFromSweepingFormula(sweeping_formula,param_sweep_settings,i_var_name):
    extra_info = {
        "default_value"  : param_sweep_settings.default_value,
        "iterations"     : param_sweep_settings.iterations,
        "i_var_name" : i_var_name,
    }
    formula_str = sweeping_formula.initialize(extra_info)
    return formula_str


# Exceptions:
class ParameterNotFoundException(Exception):
    pass
