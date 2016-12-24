# This module provides predefined formulas to use in parameter sweeping.
# We wrote this module for multiparameter sweeping as having to handle strings or "string skeletons" for multiple parameters for the same sweep would be tedious for the user.
#   Nevertheless, this functions can still be used in the uniparameter sweeping with some work.

from abc import ABC, abstractmethod    # to define abstract clasess and methods

class SweepingFormulas(ABC):
# This abstract class forces all of its subclasses to implement the "initialize" method. We need the formulas to be represented like this because
#   we want to maximize userfriendliness and for that, the parameter info has to be set programatically (default value, for example)
    @abstractmethod
    def initialize(extra_info):
        pass

class IncreasingByScalar(SweepingFormulas):
  # Example:
  #   default_value = 1900, scalar = 2 ==> 1900, 1902, 1904 ...
    def __init__(self,scalar):
        self._scalar = scalar
    def initialize(self,extra_info):
        default_value  = extra_info["default_value"]
        i_var_name = extra_info["i_var_name"]
        scalar         = self._scalar
        return "{default_value} + {i_var_name}*{scalar}".format(default_value=default_value,scalar=scalar,i_var_name=i_var_name)
    def __str__(self):
        return "IncreasingByScalar(scalar="+str(self._scalar)+")"

class IncreasingByPercentage(SweepingFormulas):
  # Example:
  #   default_value = 1, percentage = 2 ==> 1.0, 1.02, 1.04, 1.06, 1.08, 1.1, 1.12, 1.14, 1.16, 1.18,
    def __init__(self,percentage):
        self._percentage = percentage
    def initialize(self,extra_info):
        default_value = extra_info["default_value"]
        i_var_name = extra_info["i_var_name"]
        percentage    = self._percentage
        return "{default_value}*({percentage}/100*{i_var_name}+1)".format(default_value=default_value,percentage=percentage,i_var_name=i_var_name)
    def __str__(self):
        return "IncreasingByPercentage(percentage="+str(self._percentage)+")"

class DeltaBeforeAndAfter(SweepingFormulas):
  # To make the formula simpler, this function asks for #iterations to calculate the values before and after the default
  # Example:
  #   default_value = 100,iterations = 5, delta= 0.1 ==> 80.0, 90.0, 100.0, 110.0, 120.0,
    def __init__(self,delta):
        self._delta = delta
    def initialize(self,extra_info):
        default_value = extra_info["default_value"]
        iterations    = extra_info["iterations"]
        i_var_name = extra_info["i_var_name"]
        delta         = self._delta
        iterations_div_2_int = int(iterations/2)
        return "{default_value}*(1-{iterations_div_2_int}*{delta}) + {default_value}*({delta}*{i_var_name})".format(default_value=default_value,iterations_div_2_int=iterations_div_2_int,delta=delta,i_var_name=i_var_name)
    def __str__(self):
        return "DeltaBeforeAndAfter(delta="+str(self._delta)+")"

class DeltaOneUpAndOneDown(SweepingFormulas):
    ### Similar to "DeltaBeforeAndAfter" but only two iterations (Forced by exception) and doesn't include the default value
  # To make the formula simpler, this function asks for #iterations to calculate the values before and after the default
  # Example:
  #   default_value = 100,iterations = 2 (forced), delta= 0.1 ==> 90.0, 110.0
    def __init__(self,delta):
        self._delta = delta
    def initialize(self,extra_info):
        default_value = extra_info["default_value"]
        iterations    = extra_info["iterations"]
        if iterations != 2:
            # This formula needs the number of iterations to be 2 (we force it here so we don't make the code too complicated)
            raise InvalidNumberOfIterations("This formula needs to be used only in runs of 2 iterations. Iterations for this run: " + str(iterations))
        i_var_name = extra_info["i_var_name"]
        delta         = self._delta
        return "{default_value}*((1-{delta})*(1-{i_var_name}) + (1+{delta})*{i_var_name})".format(default_value=default_value,delta=delta,i_var_name=i_var_name)
    def __str__(self):
        return "DeltaBeforeAndAfter(delta="+str(self._delta)+")"

class InvalidNumberOfIterations(Exception):
    pass
