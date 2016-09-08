
import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--World3 Sensitivities Calculator--") #un logger especifico para este modulo
# Mine:
import mos_writer.mos_script_factory as mos_script_factory
import sweeping.run_and_plot_model as run_and_plot_model
import filesystem.files_aux as files_aux
import settings.settings_world3_sweep as world3_settings
import settings.gral_settings as gral_settings
import resource.standard_run_params_defaults

import mos_writer.calculate_sensitivities_mos_writer
import running.run_omc
import analysis.sensitivities_to_parameters_analysis_from_csv


#Aux for GLOBALS:

# System Dynamics .mo to use:
vanilla_SysDyn_mo_path =  world3_settings._sys_dyn_package_vanilla_path.replace("\\","/") # The System Dynamics package without modifications
piecewiseMod_SysDyn_mo_path =  world3_settings._sys_dyn_package_pw_fix_path.replace("\\","/") # Piecewise function modified to accept queries for values outside of range. Interpolate linearly using closest 2 values
populationTankNewVar_SysDyn_mo_path = world3_settings._sys_dyn_package_pop_state_var_new.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run2vermeulenAndJongh_SysDyn_mo_path= world3_settings._sys_dyn_package_v_and_j_run_2.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run3vermeulenAndJongh_SysDyn_mo_path= world3_settings._sys_dyn_package_v_and_j_run_3.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    minus_5_percent = ["reproductive_lifetime", "p_avg_life_ind_cap_1", "subsist_food_pc", "p_nr_res_use_fact_1", "p_land_yield_fact_1", "industrial_capital_init",]
    plus_5_percent =  ["p_fioa_cons_const_1", "p_ind_cap_out_ratio_1", "life_expect_norm", "des_compl_fam_size_norm", "p_serv_cap_out_ratio_1", "max_tot_fert_norm",]


    calculateValues(minus_5_percent,-5)
    calculateValues(plus_5_percent,5)

## Predefined sensitivities calculators
def calculateValues(parameters,percentage):
    print("Param name, param default, param val + (%s)" % str(percentage))
    params_info_list = resource.standard_run_params_defaults.w3_params_info_list
    for param_name,param_val in params_info_list:
        if(param_name in parameters):
            print("%s,%s,%s" % (param_name,str(param_val),str(param_val*((100+percentage)/100))))

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
