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

# CAREFUL: python vs modelica must be equivalent!! (because of differences between modelica and python we can't merge them into one)
sweeping_csv_file_name_python_skeleton = "iter_{i_str}.csv"
sweeping_csv_file_name_modelica_skeleton= """ "iter_" + String({i_name}) + ".csv";"""

#System Dynamics versions:
_sys_dyn_package_path = os.path.join(os.path.join(_resource_path,"SystemDynamics"),"package.mo") ## This one is the one that has undocumented changes (obsolete)
_sys_dyn_package_vanilla_path = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"vanilla"),"SystemDynamics"),"package.mo") # The System Dynamics package without modifications
_sys_dyn_package_pw_fix_path = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"pw_fix"),"SystemDynamics"),"package.mo") # Piecewise function modified to accept queries for values outside of range. Interpolate linearly using closest 2 values
_sys_dyn_package_pop_state_var_new = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"pop_state_var_new"),"SystemDynamics"),"package.mo") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
    # V&J paths
_sys_dyn_package_v_and_j_run_2 = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"vermeulen_and_jongh_run_2"),"SystemDynamics"),"package.mo")
_sys_dyn_package_v_and_j_run_3 = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"vermeulen_and_jongh_run_3"),"SystemDynamics"),"package.mo")
    # Pseudo ffw param and var paths:
_sys_dyn_package_pseudo_ffw_param_path = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"pseudo_ffw_param"),"SystemDynamics"),"package.mo")
_sys_dyn_package_pseudo_ffw_var_path = os.path.join(os.path.join(os.path.join(os.path.join(_resource_path,"sys_dyn"),"pseudo_ffw_var"),"SystemDynamics"),"package.mo")



#Aux:
