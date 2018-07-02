# Std
import os.path
# Mine
import settings.settings_world3_sweep as w3_settings


class IterationInfo():
    def __init__(self, i_total, sweep_params_settings_list, counter, run_folder_path):
        self.csv_file_name = w3_settings.sweeping_csv_file_name_python_skeleton.format(
            i_str=i_total)  # here we use the string skeleton for a special run instead of for any run
        self.simu_param_info_list = simulationInfoForEachParam(sweep_params_settings_list, counter)
        self.i_total = i_total
        self.swept_params = [e.param_name for e in self.simu_param_info_list]
        self.csv_path = os.path.join(run_folder_path, self.csv_file_name)


class SimulationParamInfo():
    def __init__(self, param_name, param_default, this_run_val, this_run_def_diff):
        self.param_name = param_name
        self.param_default = param_default
        self.this_run_val = this_run_val
        self.this_run_def_diff = this_run_def_diff

    def __str__(self):
        return "(param_name: " + str(simu_param_info.param_name) + ", " + "param_default: " + "{:.2f}".format(
            simu_param_info.param_default) + ", " + "this_run_val: " + "{:.2f}".format(
            simu_param_info.this_run_val) + ", " + "this_run_def_diff: " + str(simu_param_info.this_run_def_diff) + ")"

    def __repr__(self):
        return "(param_name: " + str(simu_param_info.param_name) + ", " + "param_default: " + "{:.2f}".format(
            simu_param_info.param_default) + ", " + "this_run_val: " + "{:.2f}".format(
            simu_param_info.this_run_val) + ", " + "this_run_def_diff: " + str(simu_param_info.this_run_def_diff) + ")"


# Aux
def simulationInfoForEachParam(sweep_params_settings_list, counter):
    simu_param_info_list = []
    for param_pos in range(0, len(sweep_params_settings_list)):
        param_sweep_settings = sweep_params_settings_list[param_pos]
        i_param = counter[param_pos]
        simu_param_info = simuParamInfoForParam(param_sweep_settings, i_param)
        simu_param_info_list.append(simu_param_info)
    return simu_param_info_list


def simuParamInfoForParam(param_sweep_settings, i_param):
    param_name = param_sweep_settings.param_name
    param_default = param_sweep_settings.default_value
    this_run_val = thisRunValForParam(param_sweep_settings, i_param)
    # Calculate the percentage diff (+20%, -5%, etc) to the default value
    perc = ((this_run_val * 100) / param_sweep_settings.default_value) - 100
    perc_sign_str = "-" if perc < 0 else "+" if perc > 0 else ""  # "-"  for -3, "+" for "43" and "" for 0
    this_run_def_diff = "{perc_sign_str}{perc_abs}%".format(perc_sign_str=perc_sign_str, perc_abs=int(abs(perc)))

    simu_param_info = SimulationParamInfo(param_name, param_default, this_run_val, this_run_def_diff)
    return simu_param_info


def thisRunValForParam(param_sweep_settings, i_param):
    # Set the free variable as "i" and set it using eval below
    i = i_param
    formula = param_sweep_settings.formula("i")
    val = eval(formula)  # this eval uses the free variable i
    return val
