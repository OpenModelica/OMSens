# This module provides predefined formulas to use in parameter sweeping.
# Its output is a string with a(n) (optional) free variable "i" that will be instantiated in the .mos script. Example: "1900 + i*2".
# We wrote this module for multiparameter sweeping as having to handle strings or "string skeletons" for multiple parameters for the same sweep would be tedious for the user.
#   Nevertheless, this functions can still be used in the uniparameter sweeping replacing the strings present in the respective module.

def increasingByScalar(default_value,scalar):
    # Example:
    #   default_value = 1900, scalar = 2 ==> 1900, 1902, 1904 ...
    return "{default_value} + i*{scalar}".format(default_value=default_value,scalar=scalar)

def increasingByPercentage(default_value,percentage):
    # Example:
    #   default_value = 1, percentage = 2 ==> 1.0, 1.02, 1.04, 1.06, 1.08, 1.1, 1.12, 1.14, 1.16, 1.18,
    return "{default_value}*({percentage}/100*i+1)".format(default_value=default_value,percentage=percentage)

def deltaBeforeAndAfter(default_value,iterations,delta):
    # To make the formula simpler, this function asks for #iterations to calculate the values before and after the default
    # Example:
    #   default_value = 100,iterations = 5, delta= 0.1 ==> 80.0, 90.0, 100.0, 110.0, 120.0,
    iterations_div_2_int = int(iterations/2)
    return "{default_value}*(1-{iterations_div_2_int}*{delta}) + {default_value}*({delta}*i)".format(default_value=default_value,iterations_div_2_int=iterations_div_2_int,delta=delta)
