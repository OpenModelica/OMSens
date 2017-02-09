# Std:
import os
import sys
import logging #en reemplazo de los prints
import functools # for reduce
logger = logging.getLogger("--World3 scenarios sweep--") #un logger especifico para este modulo
logger = logging.getLogger("--World3 scenarios Multiparameter sweep --") #un logger especifico para este modulo

#Mine:
import settings.settings_world3_sweep as world3_settings
import mos_writer.formulas as predef_formulas
import mos_writer.parameter_sweep_settings as parameter_sweep_settings
import mos_writer.mos_script_factory
import filesystem.files_aux as files_aux
import settings.gral_settings as gral_settings
import running.run_omc
import sweeping.iterationInfo
import readme_writer.readme_writer as readme_writer
import plotting.plot_csv as plot_csv

vanilla_SysDyn_mo_path               = world3_settings._sys_dyn_package_vanilla_path.replace("\\","/") # The System Dynamics package without modifications
piecewiseMod_SysDyn_mo_path          = world3_settings._sys_dyn_package_pw_fix_path.replace("\\","/") # Piecewise function modified to accept queries for values outside of range. Interpolate linearly using closest 2 values
populationTankNewVar_SysDyn_mo_path  = world3_settings._sys_dyn_package_pop_state_var_new.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run2vermeulenAndJongh_SysDyn_mo_path = world3_settings._sys_dyn_package_v_and_j_run_2.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
Run3vermeulenAndJongh_SysDyn_mo_path = world3_settings._sys_dyn_package_v_and_j_run_3.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it
pseudoffwparam_SysDyn_mo_path        = world3_settings._sys_dyn_package_pseudo_ffw_param_path.replace("\\","/") # Added a new "population" var that includes an integrator. Numerically it's the same as "population" but with the advantage that now we can calculate sensitivities for it

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#### WORK PACKAGE 1 ####
    # testNRResources()
#### WORK PACKAGE 3 ####
    # test3Params()
    # test3fromTop12RelativeWP2()
    # test12fromTop12RelativeWP2OneUpOneDown()
    # nrResourcesInitCurvi()
    # hugoScolnikParamsCurvi01()
    # hugoScolnikParamsCurvi02()
    # relativeTop12ParamsNoSweep5Percent()
    # relativeTop12ParamsNoSweep1Percent()
    relativeTop18ParamsNoSweep3Percent()
### WP3: no sweeps ###
    # change2For2000and2For2100RelativeTop()
    # relativeTop2for2100AndTop8For2000()
def relativeTop18ParamsNoSweep3Percent():
# Curvi run:
    # Optimum x0:
# Param name              & Default         & CurviVal3%        & Curvival3%/Default
# p_fioa_cons_const_1     & 0.43            & 0.442899987695998 & 1.0299999713860417
# p_ind_cap_out_ratio_1   & 3.0             & 3.0899999140853   & 1.0299999713617667
# reproductive_lifetime   & 30.0            & 29.1000008583085  & 0.9700000286102833
# life_expect_norm        & 28.0            & 28.8399991989023  & 1.029999971389368
# des_compl_fam_size_norm & 3.8             & 3.91399989128112  & 1.0299999713897685
# p_avg_life_ind_cap_1    & 14.0            & 13.5800004167702  & 0.9700000297693
# subsist_food_pc         & 230.0           & 223.100006581901  & 0.9700000286169609
# p_serv_cap_out_ratio_1  & 1.0             & 1.02999996814411  & 1.02999996814411
# max_tot_fert_norm       & 12.0            & 12.35999965249    & 1.0299999710408334
# p_nr_res_use_fact_1     & 1.0             & 0.970000028610385 & 0.970000028610385
# nr_resources_init       & 1000000000000.0 & 1029999970165.11  & 1.02999997016511
# p_land_yield_fact_1     & 1.0             & 1.01267089341769  & 1.01267089341769
# pop2_init               & 700000000.0     & 720999977.481686  & 1.02999996783098
# industrial_capital_init & 210000000000.0  & 203700006501.859  & 0.9700000309612333
# pot_arable_land_tot     & 3200000000.0    & 3104000158.43538  & 0.9700000495110562
# p_avg_life_serv_cap_1   & 20.0            & 19.400001917118   & 0.9700000958559001
# pot_arable_land_init    & 2300000000.0    & 2368999933.94436  & 1.0299999712801564
# pop1_init               & 650000000.0     & 669499934.855496  & 1.0299998997776862
# With:
# f=  -11515475440.7037   (negated)
#  ier =   2 nfu =  3289 nit =     21


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"      , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"    , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("reproductive_lifetime"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("life_expect_norm"         , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("des_compl_fam_size_norm"  , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.03), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("subsist_food_pc"          , predef_formulas.IncreasingByDeltaNotInclusive(-0.03), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_serv_cap_out_ratio_1"   , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("max_tot_fert_norm"        , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_nr_res_use_fact_1"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"        , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_land_yield_fact_1"      , predef_formulas.IncreasingByDeltaNotInclusive( 0.01267089341769   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop2_init"                , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("industrial_capital_init"  , predef_formulas.IncreasingByDeltaNotInclusive(-0.03 ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_tot"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.03 ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_serv_cap_1"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.03 ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_init"     , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop1_init"                , predef_formulas.IncreasingByDeltaNotInclusive( 0.03), 1),    # (param_name , formula_instance , iterations)
                                 ]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [2025,2050,2075] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def relativeTop12ParamsNoSweep1Percent():
#                            DEFAULT            Value WP2(5%, not 1%)      Curvi Results        Description
#     max_tot_fert_norm       & 12.0           & 12.60                    & 12.1199998842193   & "Normal maximal total fertility"                                 \\
#     p_fioa_cons_const_1     & 0.43           & 0.45                     & 0.434299995889143  & "Default frac of industrial output allocated to consumption" \\
#     p_ind_cap_out_ratio_1   & 3.0            & 3.15                     & 3.02999996986311   & "Default industrial capital output ratio"                        \\
#     p_serv_cap_out_ratio_1  & 1.0            & 1.05                     & 1.00999999046000   & "Default fraction of service sector output ratio"                \\
#     life_expect_norm        & 28.0           & 29.40                    & 28.2799997316718   & "Normal life expectancy"                                         \\
#     des_compl_fam_size_norm & 3.8            & 4.00                     & 3.83799996359204   & "Desired normal complete family size"                            \\
#     industrial_capital_init & 210000000000.0 & 199500000000.0           & 207900018721.344   & "Initial industrial investment"                       \\
# x   p_land_yield_fact_1     & 1.0            & 0.95                     & 0.990001558054131  & "Default land yield factor"                           \\
#     p_nr_res_use_fact_1     & 1.0            & 0.95                     & 0.990000010442315  & "Default non-recoverable resource utilization factor" \\
#     reproductive_lifetime   & 30.0           & 28.5                     & 29.7000002862185   & "Reproductive life time"                              \\
#     subsist_food_pc         & 230.0          & 218.5                    & 227.700002194902   & "Available per capita food"                           \\
#     p_avg_life_ind_cap_1    & 14.0           & 13.29                    & 13.8600001336145   & "Default average life of industrial capital";         \\
# Curvi run:
    # Optimum x0:
#    (in the table above)
# With:
# ier =   2 nfu =  2623 nit =     33
# And +-1% of boundaries
    maxTotFertNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas . IncreasingByDeltaNotInclusive(0.01 ), 1) # (param_name , formula_instance , iterations)
    fioaConsConst1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas . IncreasingByDeltaNotInclusive(0.01 ), 1) # (param_name , formula_instance , iterations)
    indCapOutRatio1_sweepSettings  = parameter_sweep_settings     . OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas . IncreasingByDeltaNotInclusive(0.01 ), 1) # (param_name , formula_instance , iterations)
    servCapOutRatio1_sweepSettings  = parameter_sweep_settings    . OrigParameterSweepSettings("p_serv_cap_out_ratio_1"  , predef_formulas . IncreasingByDeltaNotInclusive(0.01 ), 1) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("life_expect_norm"        , predef_formulas . IncreasingByDeltaNotInclusive(0.01 ), 1) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings  = parameter_sweep_settings . OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas . IncreasingByDeltaNotInclusive(0.01 ), 1) # (param_name , formula_instance , iterations)
    indCapInit_sweepSettings  = parameter_sweep_settings          . OrigParameterSweepSettings("industrial_capital_init" , predef_formulas . IncreasingByDeltaNotInclusive(-0.01), 1) # (param_name , formula_instance , iterations)
    landYieldFact1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(-0.01), 1) # (param_name , formula_instance , iterations)
    nrResUseFact1_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("p_nr_res_use_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(-0.01), 1) # (param_name , formula_instance , iterations)
    reproLifetime_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas . IncreasingByDeltaNotInclusive(-0.01), 1) # (param_name , formula_instance , iterations)
    subsistFoodPc_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("subsist_food_pc"         , predef_formulas . IncreasingByDeltaNotInclusive(-0.01), 1) # (param_name , formula_instance , iterations)
    avgLifeIndCap1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas . IncreasingByDeltaNotInclusive(-0.01), 1) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [maxTotFertNorm_sweepSettings, fioaConsConst1_sweepSettings, indCapOutRatio1_sweepSettings, servCapOutRatio1_sweepSettings, lifeExpectNorm_sweepSettings, desComplFamSizeNorm_sweepSettings, indCapInit_sweepSettings, landYieldFact1_sweepSettings, nrResUseFact1_sweepSettings, reproLifetime_sweepSettings, subsistFoodPc_sweepSettings, avgLifeIndCap1_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [2025,2050,2075] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)

def relativeTop12ParamsNoSweep5Percent():
# Table from WP2 + curvi results (the ones with an x differ between "individual" (wp2) and "together" (curvi)
#                            DEFAULT            Value WP2         Curvi Results        Description
#     max_tot_fert_norm       & 12.0           & 12.60          & 12.5999994203700  & "Normal maximal total fertility"                                 \\
#     p_fioa_cons_const_1     & 0.43           & 0.45           & 0.448380420759870 & "Default frac of industrial output allocated to consumption" \\
#     p_ind_cap_out_ratio_1   & 3.0            & 3.15           & 3.14999863042567  & "Default industrial capital output ratio"                        \\
#     p_serv_cap_out_ratio_1  & 1.0            & 1.05           & 1.04559432323735  & "Default fraction of service sector output ratio"                \\
#     life_expect_norm        & 28.0           & 29.40          & 29.3999986573765  & "Normal life expectancy"                                         \\
#     des_compl_fam_size_norm & 3.8            & 4.00           & 3.98999981851597  & "Desired normal complete family size"                            \\
#     industrial_capital_init & 210000000000.0 & 199500000000.0 & 199499999088.315  & "Initial industrial investment"                       \\
# x   p_land_yield_fact_1     & 1.0            & 0.95           & 1.04989368154214  & "Default land yield factor"                           \\
#     p_nr_res_use_fact_1     & 1.0            & 0.95           & 0.949999988082543 & "Default non-recoverable resource utilization factor" \\
#     reproductive_lifetime   & 30.0           & 28.5           & 28.4999996571028  & "Reproductive life time"                              \\
#     subsist_food_pc         & 230.0          & 218.5          & 218.499997333924  & "Available per capita food"                           \\
# x   p_avg_life_ind_cap_1    & 14.0           & 13.29          & 14.6999966717931  & "Default average life of industrial capital";         \\
# Curvi run:
    # Optimum x0:
#    (in the table above)
# With:
# ier =   2 nfu =  2623 nit =     33
# And +-5% of boundaries
    maxTotFertNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas . IncreasingByDeltaNotInclusive(0.0499999516975    ), 1) # (param_name , formula_instance , iterations)
    fioaConsConst1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas . IncreasingByDeltaNotInclusive(0.0427451645578372 ), 1) # (param_name , formula_instance , iterations)
    indCapOutRatio1_sweepSettings  = parameter_sweep_settings     . OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas . IncreasingByDeltaNotInclusive(0.0499995434752234 ), 1) # (param_name , formula_instance , iterations)
    servCapOutRatio1_sweepSettings  = parameter_sweep_settings    . OrigParameterSweepSettings("p_serv_cap_out_ratio_1"  , predef_formulas . IncreasingByDeltaNotInclusive(0.04559432323735   ), 1) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("life_expect_norm"        , predef_formulas . IncreasingByDeltaNotInclusive(0.0499999520491607 ), 1) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings  = parameter_sweep_settings . OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas . IncreasingByDeltaNotInclusive(0.0499999522410448 ), 1) # (param_name , formula_instance , iterations)
    indCapInit_sweepSettings  = parameter_sweep_settings          . OrigParameterSweepSettings("industrial_capital_init" , predef_formulas . IncreasingByDeltaNotInclusive(-0.05              ), 1) # (param_name , formula_instance , iterations)
    landYieldFact1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(0.04989368154214   ), 1) # (param_name , formula_instance , iterations)
    nrResUseFact1_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("p_nr_res_use_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(-0.05              ), 1) # (param_name , formula_instance , iterations)
    reproLifetime_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas . IncreasingByDeltaNotInclusive(-0.05              ), 1) # (param_name , formula_instance , iterations)
    subsistFoodPc_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("subsist_food_pc"         , predef_formulas . IncreasingByDeltaNotInclusive(-0.05              ), 1) # (param_name , formula_instance , iterations)
    avgLifeIndCap1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas . IncreasingByDeltaNotInclusive(0.0499997622709356 ), 1) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [maxTotFertNorm_sweepSettings, fioaConsConst1_sweepSettings, indCapOutRatio1_sweepSettings, servCapOutRatio1_sweepSettings, lifeExpectNorm_sweepSettings, desComplFamSizeNorm_sweepSettings, indCapInit_sweepSettings, landYieldFact1_sweepSettings, nrResUseFact1_sweepSettings, reproLifetime_sweepSettings, subsistFoodPc_sweepSettings, avgLifeIndCap1_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [2025,2050,2075] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def hugoScolnikParamsCurvi02():
# Hugo Scolnik article: "Crítica metodológica al modelo WORLD 3" (Methodological criticisim to the World3 model)
#   Perturbed 5 params by 5%
      # ICOR= 3.15, Default: ICOR=3
      # ALIC= 13.3, Default: ALIC=14
      # ALSC= 17.1, Default: ALSC=20
      # SCOR= 1.05, Default: SCOR=1
      # Run "Perturbed": FFW= 0.231, Default: FFW=0.22
      # Run "Perturbed Increasing FFW": FFW= 0.242, Default: FFW=0.22
#   Perturbed rest of the params by a scalar of 0.24172080E-12
# This function is based in the results of curvi+w3:
    # Optimum x0:
#    p_ind_cap_out_ratio_1  - 3.15 ==> +5%
#    p_avg_life_ind_cap_1   - 13.3 ==> -5%
#    p_avg_life_serv_cap_1  - 19.0 ==> -5%
#    p_serv_cap_out_ratio_1 - 1.05 ==> +5%
# With:
# ier = 2 nfu = 1964 nit = 93 fopt = -9985562545.07286
# And +-5% of boundaries
    icor_sweepSettings  = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"  , predef_formulas.IncreasingByPercentage(5), 2) # (param_name , formula_instance , iterations)
    ialic_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"   , predef_formulas.IncreasingByPercentage(-5), 2) # (param_name , formula_instance , iterations)
    ialsc_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_serv_cap_1"  , predef_formulas.IncreasingByPercentage(-5), 2) # (param_name , formula_instance , iterations)
    iscor_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_serv_cap_out_ratio_1" , predef_formulas.IncreasingByPercentage(5), 2) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [ icor_sweepSettings, ialic_sweepSettings, ialsc_sweepSettings, iscor_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [2025,2050,2075] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def hugoScolnikParamsCurvi01():
# Hugo Scolnik article: "Crítica metodológica al modelo WORLD 3" (Methodological criticisim to the World3 model)
#   Perturbed 5 params by 5%
      # ICOR= 3.15, Default: ICOR=3
      # ALIC= 13.3, Default: ALIC=14
      # ALSC= 17.1, Default: ALSC=20
      # SCOR= 1.05, Default: SCOR=1
      # Run "Perturbed": FFW= 0.231, Default: FFW=0.22
      # Run "Perturbed Increasing FFW": FFW= 0.242, Default: FFW=0.22
#   Perturbed rest of the params by a scalar of 0.24172080E-12
# This function is based in the results of curvi+w3:
    # Optimum x0:
    # p_ind_cap_out_ratio_1  - 3.93944837212699...  Default: ICOR=3     ==> +31%
    # p_avg_life_ind_cap_1   - 14.4095197725215...  Default: ALIC=14    ==> +03%
    # p_avg_life_serv_cap_1  - 24.8371810528411...  Default: ALSC=20    ==> +24%
    # p_serv_cap_out_ratio_1 - 0.500018268440072..  Default: SCOR=1     ==> -50%
# With:
# ier = 2 nfu = 1964 nit = 93 fopt = -9985562545.07286
# And with big boundaries (~50%)



    icor_sweepSettings  = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"  , predef_formulas.IncreasingByPercentage(16)  , 3) # (param_name , formula_instance , iterations)
    ialic_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"   , predef_formulas.IncreasingByPercentage(0.015) , 3) # (param_name , formula_instance , iterations)
    ialsc_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_serv_cap_1"  , predef_formulas.IncreasingByPercentage(12)  , 3) # (param_name , formula_instance , iterations)
    iscor_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_serv_cap_out_ratio_1" , predef_formulas.IncreasingByPercentage(-25) , 3) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [ icor_sweepSettings, ialic_sweepSettings, ialsc_sweepSettings, iscor_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def nrResourcesInitCurvi():
# Curvi run with:
#       parameter= nr_resources_init
#       variable to optimize = population
#       x0 = (/1000000000000.0D0/)
#       n = 1
#       eps=1.d-10
#       ibound=1
#       jbound(1)=3      ! 0 if the ith variable has no constraints.
# c                        1 if the ith variable has only upper bounds.
# c                        2 if the ith variable has only lower bounds.
# c                        3 if the ith variable has both upper and lower bounds
#       bl(1)=1000D0     ! lower bound of x0(1) (depends on ibound and jbound)
#       bu(1)=2000000000000.0D0    ! upper bound of x0(1)  (depends on ibound and jbound)
#       nfu=1000         ! <--- MAX NUMBER OF CALLS TO FU
#       idiff=2
#       kmax=3



    nRResInit_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"      , predef_formulas.IncreasingByPercentageNotInclusive(8), 5) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [nRResInit_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def relativeTop2for2100AndTop8For2000():
# We try to increase the population for both 2100 and 2000 to try and fit the function between 1900 and 2000 and still have an effect on 2100
# Top 2 for 2100 up and top 3-8 for 2000 also up (to try and revert the (-) effect on those top 2). Some of these "top 3-8" for 2000 have a negative effect in 2100.

# Parameter             |   Position in 2000 sorted for pop | Position in 2100 sorted for pop
# p_fioa_cons_const_1       1  (-0.1896934079)                1  (0.4367021008)
# p_ind_cap_out_ratio_1     2  (-0.1590716648)                2  (0.30914336)
# p_avg_life_ind_cap_1      3  (0.0880944114)                 6  (-0.0982760653)
# reproductive_lifetime     4  (-0.0598396094)                3  (-0.1321867349)   <- we affect this one negatively (-5%)
# land_fr_harvested         5  (0.0549721817)                 20 (-0.0083348982)
# inherent_land_fert        6  (0.0511521159)                 21 (-0.0080056655)
# p_land_yield_fact_1       7  (0.0508257086)                 12 (-0.0269650958)
# des_compl_fam_size_norm   8  (0.0477282242)                 5  (0.1060414143)

    fioaConsConst_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    indCapOutRat_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    avgLifeIndCap_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    reproLifet_sweepSettings          = parameter_sweep_settings.OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas.IncreasingByPercentageNotInclusive(-5), 1) # (param_name , formula_instance , iterations)
    landFrHarvested_sweepSettings     = parameter_sweep_settings.OrigParameterSweepSettings("land_fr_harvested"       , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    inherentLandFert_sweepSettings    = parameter_sweep_settings.OrigParameterSweepSettings("inherent_land_fert"      , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    landYieldFact1_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [fioaConsConst_sweepSettings, indCapOutRat_sweepSettings, avgLifeIndCap_sweepSettings, reproLifet_sweepSettings, landFrHarvested_sweepSettings, inherentLandFert_sweepSettings, landYieldFact1_sweepSettings, desComplFamSizeNorm_sweepSettings,]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","ppoll_index","industrial_output","nr_resources","food"],
    "stopTime"                   : 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [1940] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)

def relativeTop2for2100AndManyPositiveFor2000():
# We try to increase the population for 2100 and decrease it for 2000 to try and fit the function between 1900 and 2000 and still have an effect on 2100
# Top 2 for 2100 up and only the positive in both up. The Top 2 for 2100 affect the one in 2000 negatively so we try to revert those changes with only positive for 2000 (that are also positive in 2100)


# Parameter             |   Position in 2000 sorted for pop | Position in 2100 sorted for pop
# p_fioa_cons_const_1       1  (-0.1896934079)                1  (0.4367021008)
# p_ind_cap_out_ratio_1     2  (-0.1590716648)                2  (0.30914336)
# life_expect_norm          11 (0.0305075556)                 4  (0.1315758044)
# des_compl_fam_size_norm   8  (0.0477282242)                 5  (0.1060414143)
# max_tot_fert_norm         18 (0.009409269)                  9  (0.0345123911)
# lifet_perc_del            22 (0.0044847922)                 22 (0.0068062731)
# avg_life_land_norm        26 (0.0020099261)                 28 (0.0037855243)
# ppoll_in_1970             29 (0.0012835169)                 31 (0.0027901066)
# income_expect_avg_time    21 (0.0050549969)                 33 (0.0018008269)
# social_adj_del            24 (0.003111505)                  34 (0.0016976242)

    fioaConsConst_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    indCapOutRat_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("life_expect_norm"        , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    maxTotFertNorm_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    lifetPercDel_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("lifet_perc_del"          , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    avgLifeLandNorm_sweepSettings     = parameter_sweep_settings.OrigParameterSweepSettings("avg_life_land_norm"      , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    ppollIn1970_sweepSettings         = parameter_sweep_settings.OrigParameterSweepSettings("ppoll_in_1970"           , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    incomeExpectAvgTime_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("income_expect_avg_time"  , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
    socialAdjDel_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("social_adj_del"          , predef_formulas.IncreasingByPercentageNotInclusive(5), 1) # (param_name , formula_instance , iterations)
# Add the sweepSettings to the following list
    sweep_params_settings_list   = [ fioaConsConst_sweepSettings, indCapOutRat_sweepSettings, lifeExpectNorm_sweepSettings, desComplFamSizeNorm_sweepSettings, maxTotFertNorm_sweepSettings,lifetPercDel_sweepSettings, avgLifeLandNorm_sweepSettings, ppollIn1970_sweepSettings, incomeExpectAvgTime_sweepSettings, socialAdjDel_sweepSettings,]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    }
    setUpSweepsAndRun(**run_kwargs)
### WP 3 tests ####
def test12fromTop12RelativeWP2OneUpOneDown():

    # Declare each parameter settings separately and then add them to the list manually
# Con one up one down
    indCapInit_sweepSettings          = parameter_sweep_settings.OrigParameterSweepSettings("industrial_capital_init" , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
# Orig
    landYieldFact_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    nRResUseFact_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("p_nr_res_use_fact_1"     , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    reproLifet_sweepSettings          = parameter_sweep_settings.OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    subsistFood_sweepSettings         = parameter_sweep_settings.OrigParameterSweepSettings("subsist_food_pc"         , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    avgLifeIndCap_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    maxTotFertNorm_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    fioaConsConst_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    indCapOutRat_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    servCapOutRatio_sweepSettings     = parameter_sweep_settings.OrigParameterSweepSettings("p_serv_cap_out_ratio_1"  , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("life_expect_norm"        , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
    sweep_params_settings_list   = [indCapInit_sweepSettings, landYieldFact_sweepSettings, nRResUseFact_sweepSettings, reproLifet_sweepSettings, subsistFood_sweepSettings, avgLifeIndCap_sweepSettings, maxTotFertNorm_sweepSettings, fioaConsConst_sweepSettings, indCapOutRat_sweepSettings, servCapOutRatio_sweepSettings, lifeExpectNorm_sweepSettings, desComplFamSizeNorm_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : False, #Choose to plot std run alognside this test results
    }
    setUpSweepsAndRun(**run_kwargs)

def test3fromTop12RelativeWP2():

    # Declare each parameter settings separately and then add them to the list manually
    fioaConsConst_sweepSettings  = parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"   , predef_formulas.DeltaBeforeAndAfter(0.01) , 5) # (param_name , formula_instance , iterations)
    indCapOutRat_sweepSettings   = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1" , predef_formulas.DeltaBeforeAndAfter(0.01) , 5) # (param_name , formula_instance , iterations)
    reproLifet_sweepSettings     = parameter_sweep_settings.OrigParameterSweepSettings("reproductive_lifetime" , predef_formulas.DeltaBeforeAndAfter(0.01) , 5) # (param_name , formula_instance , iterations)
    sweep_params_settings_list   = [ fioaConsConst_sweepSettings, indCapOutRat_sweepSettings, reproLifet_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : False, #Choose to plot std run alognside this test results
    }
    setUpSweepsAndRun(**run_kwargs)

def test3Params():

    inExAvgTim_sweepSettings   = parameter_sweep_settings.OrigParameterSweepSettings("income_expect_avg_time" , predef_formulas.DeltaBeforeAndAfter(0.01) , 5) # (param_name , formula_instance , iterations)
    indCapOutRat_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"  , predef_formulas.IncreasingByPercentage(5) , 2) # (param_name , formula_instance , iterations)
    nRResInit_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"      , predef_formulas.DeltaBeforeAndAfter(0.1)  , 5) # (param_name , formula_instance , iterations)
    sweep_params_settings_list = [ inExAvgTim_sweepSettings, indCapOutRat_sweepSettings,nRResInit_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : False, #Choose to plot std run alognside this test results
    }
    setUpSweepsAndRun(**run_kwargs)
### WP 1 tests ####
def testNRResources():
    nRResInit_sweepSettings   = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init" , predef_formulas.DeltaBeforeAndAfter(0.1) , 10) # (param_name , formula_instance , iterations)
    sweep_params_settings_list = [ nRResInit_sweepSettings ]
    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars":["Food_Production1Agr_InpIntegrator1y","Arable_Land_Dynamics1Pot_Arable_LandIntegrator1y","Arable_Land_Dynamics1Arable_LandIntegrator1y","population","nr_resources"], # Examples: SPECIAL_policy_years, ["nr_resources_init"]
    "stopTime": 2100  ,# year to end the simulation (2100 for example)
    "scens_to_run" : [1], #The standard run corresponds to the first scenario
    "fixed_params" : [],  # No fixed parameter changes. Example: [("nr_resources_init",6.3e9),("des_compl_fam_size_norm",2),...]
    "mo_file" : vanilla_SysDyn_mo_path, # Mo without modifications
    "plot_std_run": False, #Choose to plot std run alognside this test results
    }
    setUpSweepsAndRun(**run_kwargs)

# Functions:

def setUpSweepsAndRun(sweep_params_settings_list,fixed_params,plot_vars,stopTime,scens_to_run,mo_file,plot_std_run,fixed_params_description_str=False,extra_ticks=[]):
    startTime = 1900 # year to start the simulation. Because W3-Mod needs the starttime to be always 1900, we don't allow the user to change it
    #The "root" output folder path.
    output_root_path = files_aux.makeOutputPath("modelica_multiparam_sweep")
    #Create scenarios from factory
    scenarios = []
    for scen_num in scens_to_run:
        folder_name = "scenario_"+str(scen_num)
        logger.info("Running scenario {folder_name}".format(folder_name=folder_name))
        # Create main folder
        scen_folder_path = os.path.join(output_root_path,folder_name)
        os.makedirs(scen_folder_path)
        # Create run folder
        run_folder_path  = os.path.join(scen_folder_path,"run")
        os.makedirs(run_folder_path)
        # Write 2 copies of the output mos_path: one in the root folder of the scenario and the other inside the 'run' folder. The second one will be the one being executed.
        output_mos_copy_path = os.path.join(scen_folder_path,gral_settings.mos_script_filename)
        output_mos_tobeExe_path = os.path.join(run_folder_path,gral_settings.mos_script_filename)
        model_name = world3_settings._world3_scenario_model_skeleton.format(scen_num=scen_num)
        multiparamMosWriter = mos_writer.sweeping_mos_writer.MultiparamSweepingMosWriter()
        multiparamMosWriter.createMos(model_name, startTime, stopTime, mo_file, sweep_params_settings_list, fixed_params, output_mos_tobeExe_path, world3_settings.sweeping_csv_file_name_modelica_skeleton,mos_copy_path=output_mos_copy_path)
        # Write run settings:
        run_settings = {
            "sweep_params_settings_list": sweep_params_settings_list,
            "fixed_params": fixed_params,
            "plot_vars": plot_vars,
            "stopTime": stopTime,
            "scen_num": scen_num,
            "model_name": model_name,
            "mo_file": mo_file,
            "plot_std_run": plot_std_run,
            "fixed_params_description_str":fixed_params_description_str,
        }
        writeRunLog(run_settings, os.path.join(scen_folder_path,gral_settings.omc_creation_settings_filename))
        # Run
        running.run_omc.runMosScript(output_mos_tobeExe_path)
        # Get iterations info per param per iteration
        iterationsInfo_list = iterationsInfoForThisRun(sweep_params_settings_list,run_folder_path)
        # Plot desired variables
        plots_folder_path =os.path.join(scen_folder_path,"plots")
        os.makedirs(plots_folder_path)
        # If the fixed params description has not been set (if there are a lot of params changed fixed then a custom description may be advantageous) then make the default one
        if not fixed_params_description_str:
            # If there are no fixed params for this run then just write "None" or similar
            if len(fixed_params) == 0:
                fixed_params_description_str = "None"
            # If there is at least one fixed param, write them separated by commas.
            else:
                fixed_params_description_str = ", ".join([str(x) for x in fixed_params])
        plot_csv.plotVarsFromIterationsInfo(plot_vars,model_name,iterationsInfo_list,plots_folder_path,plot_std_run,fixed_params_description_str,extra_ticks)
        # Write automatic readme (with general info and specific info for this sweep)
        readme_path = os.path.join(scen_folder_path,gral_settings.readme_filename)
        readme_writer.writeReadmeMultiparam(readme_path,iterationsInfo_list)

    # setUpSweepsAndRun(**kwargs)
def iterationsInfoForThisRun(sweep_params_settings_list,run_folder_path):
    # We iterate the params in the same order in which they will be iteratted in the fors in the .mos script.
    # For each "total" iteration, each parameter will have it's own "i" set in a value and from that personal "i" and their formula they will calculate their value for the simulation corresponding to this run
    # Here, we will calculate each of those values but in python instead of in Modelica
#     iterationInfo():
# import  simulationParamInfo():
    itersTotal = functools.reduce(lambda accum,e: accum*e, [e.iterations for e in sweep_params_settings_list], 1)

    iterationsInfo_list = []

    counter = [0] * len(sweep_params_settings_list)   # for each param, we keep a count of its internal iterator in this list
    for i_total in range(itersTotal):
        # Calculate the info of each parameter for this iteration
        iterInfo = sweeping.iterationInfo.IterationInfo(i_total, sweep_params_settings_list, counter,run_folder_path)

        # Add 1 to the last param
        counter[len(counter)-1] = counter[len(counter)-1] +1
        # Check if the last params and its predecessors reached their max ( max = #iterations)
        pos = len(counter) -1
        while(counter[pos] == sweep_params_settings_list[pos].iterations and pos > 0):
            counter[pos] = 0   # restart the counter for current pos
            pos = pos -1       # go to previous pos
            counter[pos] = counter[pos] +1    # add 1 to previous pos
        iterationsInfo_list.append(iterInfo)
    return iterationsInfo_list



def writeRunLog(run_settings_dict, output_path):
    intro_str = """The whole "create mos, run it and plot it" script was run with the following settings"""+"\n"
    format_explanation_str = """<setting_name>:\n   <setting_value>"""+"\n"
    all_settings = []
    for setting_name,setting_value in run_settings_dict.items():
        setting_str = """{setting_name}:\n {setting_value}""".format(setting_name=setting_name,setting_value=str(setting_value))
        all_settings.append(setting_str)
    all_settings_str = "\n".join(all_settings)
    final_str = intro_str + format_explanation_str + "\n" + all_settings_str
    files_aux.writeStrToFile(final_str,output_path)
    return 0
def initialFactoryForWorld3ScenarioMultiparamSweep(scen_num,stop_time,mo_file,sweep_params_settings_list,fixed_params=[]):
    #Get the mos script factory for a scenario number (valid from 1 to 11)
    model_name = world3_settings._world3_scenario_model_skeleton.format(scen_num=scen_num) #global
    initial_factory_dict = {
        "model_name"                 : model_name,
        "startTime"                  : 1900, # year to start the simulation. Because W3-Mod needs the starttime to be always 1900, we don't allow the user to change it
        "stopTime"                   : stop_time,
        "mo_file"                    : mo_file,
        "sweep_params_settings_list" : sweep_params_settings_list,
        "fixed_params"               : fixed_params,
        }
    initial_factory = mos_writer.mos_script_factory.MultiparamMosScriptFactory(settings_dict=initial_factory_dict)
    return initial_factory

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
