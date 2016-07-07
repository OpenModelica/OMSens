import inspect
import os
#Mine
import filesystem.files_aux as files_aux
# General settings for World3 sweeps
_world3_scenario_model_skeleton = "SystemDynamics.WorldDynamics.World3.Scenario_{scen_num}"
_currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
_parentdir = files_aux.parentDir(_currentdir)
_resource_path =os.path.join(_parentdir,"resource")
_std_run_csv = os.path.join(_resource_path,"standard_run.csv")

# CAREFUL: both must be equivalent!! (because of differences between modelica and python we can't merge them into one)
csv_file_name_python_skeleton = "iter_{i_str}.csv"
csv_file_name_modelica_skeleton= """ "iter_" + String(i) + ".csv";"""

#System Dynamics versions:
_sys_dyn_package_path = os.path.join(os.path.join(_resource_path,"SystemDynamics"),"package.mo")
_sys_dyn_package_pw_fix_path = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"pw_fix"),"SystemDynamics"),"package.mo")
_sys_dyn_package_vanilla_path = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"vanilla"),"SystemDynamics"),"package.mo")
_sys_dyn_package_pop_state_var_new = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"pop_state_var_new"),"SystemDynamics"),"package.mo")
