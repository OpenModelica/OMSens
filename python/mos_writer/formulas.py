# This module provides predefined formulas to use in parameter sweeping.
# We wrote this module for multiparameter sweeping as having to handle strings or "string skeletons" for multiple parameters for the same sweep would be tedious for the user.
#   Nevertheless, this functions can still be used in the uniparameter sweeping with some work.

from abc import ABC, abstractmethod  # to define abstract clasess and methods


class SweepingFormulas(ABC):
    # This abstract class forces all of its subclasses to implement the "initialize" method. We need the formulas to be represented like this because
    #   we want to maximize userfriendliness and for that, the parameter info has to be set programatically (default value, for example)
    @abstractmethod
    def initialize(extra_info):
        pass


class IncreasingByScalar(SweepingFormulas):
    # Example:
    #   default_value = 1900, scalar = 2 ==> 1900, 1902, 1904 ...
    def __init__(self, scalar):  # <--- this function is the one used explicitly in the scripts
        self._scalar = scalar

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]
        i_var_name = extra_info["i_var_name"]
        scalar = self._scalar
        return "({default_value}) + {i_var_name}*({scalar})".format(default_value=default_value, scalar=scalar,
                                                                    i_var_name=i_var_name)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "IncreasingByScalar(scalar=" + str(self._scalar) + ")"


class IncreasingByPercentage(SweepingFormulas):
    # Example:
    #   default_value = 1, percentage = 2 ==> 1.0, 1.02, 1.04, 1.06, 1.08, 1.1, 1.12, 1.14, 1.16, 1.18,
    def __init__(self, percentage):  # <--- this function is the one used explicitly in the scripts
        self._percentage = percentage

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]
        i_var_name = extra_info["i_var_name"]
        percentage = self._percentage
        return "({default_value})*(({percentage})/100*{i_var_name}+1)".format(default_value=default_value,
                                                                              percentage=percentage,
                                                                              i_var_name=i_var_name)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "IncreasingByPercentage(percentage=" + str(self._percentage) + ")"


class IncreasingByPercentageNotInclusive(SweepingFormulas):
    # Similar to IncreasingByPercentage but without including std value
    # Example:
    #   default_value = 1, percentage = 2 ==> 1.02, 1.04, 1.06, 1.08, 1.1, 1.12, 1.14, 1.16, 1.18,
    def __init__(self, percentage):  # <--- this function is the one used explicitly in the scripts
        self._percentage = percentage

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]
        i_var_name = extra_info["i_var_name"]
        percentage = self._percentage
        return "({default_value})*(({percentage})/100*({i_var_name}+1)+1)".format(default_value=default_value,
                                                                                  percentage=percentage,
                                                                                  i_var_name=i_var_name)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "IncreasingByPercentage(percentage=" + str(self._percentage) + ")"


class DeltaBeforeAndAfter(SweepingFormulas):
    # To make the formula simpler, this function asks for #iterations to calculate the values before and after the default
    # Example:
    #   default_value = 100,iterations = 5, delta= 0.1 ==> 80.0, 90.0, 100.0, 110.0, 120.0,
    def __init__(self, delta):  # <--- this function is the one used explicitly in the scripts
        self._delta = delta

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]
        iterations = extra_info["iterations"]
        i_var_name = extra_info["i_var_name"]
        delta = self._delta
        iterations_div_2_int = int(iterations / 2)
        return "({default_value})*(1-{iterations_div_2_int}*({delta})) + ({default_value})*(({delta})*{i_var_name})".format(
            default_value=default_value, iterations_div_2_int=iterations_div_2_int, delta=delta, i_var_name=i_var_name)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "DeltaBeforeAndAfter(delta=" + str(self._delta) + ")"


class DeltaOneUpAndOneDown(SweepingFormulas):
    ### Similar to "DeltaBeforeAndAfter" but only two iterations (Forced by exception) and doesn't include the default value
    # To make the formula simpler, this function asks for #iterations to calculate the values before and after the default
    # Example:
    #   default_value = 100,iterations = 2 (forced), delta= 0.1 ==> 90.0, 110.0
    def __init__(self, delta):  # <--- this function is the one used explicitly in the scripts
        self._delta = delta

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]
        iterations = extra_info["iterations"]
        if iterations != 2:
            # This formula needs the number of iterations to be 2 (we force it here so we don't make the code too complicated)
            raise InvalidNumberOfIterations(
                "This formula needs to be used only in runs of 2 iterations. Iterations for this run: " + str(
                    iterations))
        i_var_name = extra_info["i_var_name"]
        delta = self._delta
        return "({default_value})*((1-({delta}))*(1-{i_var_name}) + (1+({delta}))*{i_var_name})".format(
            default_value=default_value, delta=delta, i_var_name=i_var_name)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "DeltaBeforeAndAfter(delta=" + str(self._delta) + ")"


class IncreasingByDeltaNotInclusive(SweepingFormulas):
    ### Similar to "DeltaBeforeAndAfter" but only after and not including the std value  (may receive a negative delta and it becomes a "DecreasingByDeltaNotInclusive")
    # Example:
    #   default_value = 100,iterations = 2 , delta= 0.1 ==> 110.0, 120.0
    def __init__(self, delta):  # <--- this function is the one used explicitly in the scripts
        self._delta = delta

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]
        i_var_name = extra_info["i_var_name"]
        delta = self._delta
        return "({default_value})*(1+({delta})*({i_var_name}+1))".format(default_value=default_value, delta=delta,
                                                                         i_var_name=i_var_name)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "IncreasingByDeltaNotInclusive(delta=" + str(self._delta) + ")"


class OneValue(SweepingFormulas):
    # For when you want to set a fixed value but still want to see the difference from the default in the legend of this run (the alternative would be to instead use the "fixed_values" array to set a fixed value but this change wouldn't be taken into accound in the legend of this run in the plot)
    # Example:
    #   default_value = "anything",iterations = 1 (forced), fixed_value= 33 ==> 33
    def __init__(self, fixed_value):  # <--- this function is the one used explicitly in the scripts
        self._fixed_value = fixed_value

    def initialize(self, extra_info):
        # This function is called by the parameter sweep settings instance
        default_value = extra_info["default_value"]  # we will just ignore the default value
        iterations = extra_info["iterations"]
        if iterations != 1:
            # This formula needs the number of iterations to be 1 (we force it here so we don't make the code too complicated)
            raise InvalidNumberOfIterations(
                "This formula needs to be used only in runs of 1 iteration. Iterations set for this run: " + str(
                    iterations))
        fixed_value = self._fixed_value
        return "{fixed_value}".format(fixed_value=fixed_value)

    # (we wrap all the values in parenthesis "()" just in case the value is negative and omc doesn't like negative signs roaming around)
    def __str__(self):
        return "OneValueFormula(fixed_value=" + str(self._fixed_value) + ")"


class InvalidNumberOfIterations(Exception):
    pass
