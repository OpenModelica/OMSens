# Settings not specific to a certain script (such as the world3_sweep script)
mos_script_filename = "mos_script.mos"
omc_creation_settings_filename = "omc_creation_settings.txt"
omc_run_log_filename = "omc_run_log.txt"
readme_filename = "readme.txt"

_interpreter_windows = "%OPENMODELICAHOME%\\bin\\omc"
_interpreter_linux = "omc"


def calc_sens_csv_file_name_function(param_name):
    # The csv file name of the parameters from calculation of sensitivities needs to be a function because we have to replace the brackets ([) in python and in modelica
    standarized_param_name = removeSpecialCharactersTo(param_name)
    return "{param_name}_perturbed.csv".format(param_name=standarized_param_name)


def removeSpecialCharactersTo(param_name):
    wo_left_bracket = param_name.replace("[", "_bracket_")
    wo_both_brackets = wo_left_bracket.replace("]", "_bracket")
    standarized_param_name = wo_both_brackets
    return standarized_param_name
