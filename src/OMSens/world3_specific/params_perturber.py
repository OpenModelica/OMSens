
import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("-- Parameters perturbation calculator --") #un logger especifico para este modulo
# Mine:
import settings.settings_world3_sweep as world3_settings
import world3_specific.standard_run_params_defaults



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
    by_scalar =  ["p_fioa_cons_const_1", "p_ind_cap_out_ratio_1", "life_expect_norm", "des_compl_fam_size_norm", "p_serv_cap_out_ratio_1", "max_tot_fert_norm",]


    print(perturbeParameterByPercentage(minus_5_percent,-5))
    print(perturbeParameterByPercentage(plus_5_percent,5))
    print(perturbeParameterByAddingScalar(by_scalar,0.01))

## Predefined sensitivities calculators
def perturbeParameterByAddingScalar(parameters,scalar):
    logger.info(" Calculating perturbed values by scalar "+str(scalar)+".")
    return perturbeParameterByLambda(parameters,lambda param_val: param_val+scalar)

def perturbeParameterByPercentage(parameters,percentage):
    logger.info(" Calculating perturbed values by "+str(percentage)+"%.")
    return perturbeParameterByLambda(parameters,lambda param_val: param_val*(100+percentage)/100)

def perturbeParameterByLambda(parameters,lambda_func):
    default_params_info_list   = world3_specific.standard_run_params_defaults.w3_params_info_list
    perturbed_params_info_list = []

    logger.debug("  (<PARAM_NAME>,<PARAM_DEFAULT>,<PARAM_PERTURBED>)")
    for param_name,param_val,param_desc in default_params_info_list:
        if(param_name in parameters):
            perturbed_val = lambda_func(param_val)
            # Commented because "debug" filter was used wrongly in other modules
            logger.debug("  %s,%s,%s" % (param_name,str(param_val),str(perturbed_val)))
            perturbed_params_info_list.append((param_name,perturbed_val))
    return perturbed_params_info_list


# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
