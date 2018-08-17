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
import modelica_interface.run_omc as run_omc
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
    # hugoScolnikParamsCurvi01()
    # hugoScolnikParamsCurvi02()
    # change2For2000and2For2100RelativeTop()            # no sweep
    # relativeTop2for2100AndTop8For2000()               # no sweep
# Curvi Only Pop
    # relativeTop12ParamsNoSweep5PercentOptimizePop()   # no sweep
    # relativeTop12ParamsNoSweep1PercentOptimizePop()   # no sweep
    # relativeTop18ParamsNoSweep3PercentOptimizePop()   # no sweep
    # relativeTop36ParamsNoSweep3PercentOptimizePop()   # no sweep
    # nrResourcesInitCurviNoSweepOptimizePop()          # no sweep
    # onlyMeasurableInitValsNoSweep3PercOptimizePop()   # no sweep
    # onlyMeasurableInitValsNoSweep5PercOptimizePop()   # no sweep
    # relativeTop12ParamsSweepOf2Params5PercentOptimizePop()
# Curvi pop and hwi
    # relativeTop12ParamsNoSweep3PercentOptimizePopAndHWI() #no sweep
    # relativeTop12ParamsNoSweep5PercentOptimizePopAndHWI() #no sweep
# ZXPOWL only pop
    # nrResourcesInitZXPOWLNoSweepOptimizePop() #no sweep
#### POST - WORK PACKAGE 3 ####
# Policies Triggers  with CURVI
#   policyTriggers_test31_nosweep()  # the parameters are the policy triggers for scenarios 2 to 9. Initial: 2050
#   policyTriggers_test32_nosweep()  # the parameters are the policy triggers for scenarios 2 to 9. Initial: 2018
#   policyTriggers_test33_nosweep()  # the parameters are the policy triggers for scenarios 2 to 9. Initial: 2034
    hapzardExperiment()

##### TESTS DEFINITIONS #####
def hapzardExperiment():
    # Hapzard sweep of 4 paramet
    sweep_params_settings_list    = [
      parameter_sweep_settings      . OrigParameterSweepSettings("p_land_yield_fact_1"    , predef_formulas . DeltaBeforeAndAfter(0.05), 2), # (param_name , formula_instance , iterations)
      parameter_sweep_settings      . OrigParameterSweepSettings("p_avg_life_ind_cap_1"   , predef_formulas . DeltaBeforeAndAfter(0.05), 2), # (param_name , formula_instance , iterations)
      parameter_sweep_settings      . OrigParameterSweepSettings("p_nr_res_use_fact_1"    , predef_formulas . DeltaBeforeAndAfter(0.05), 2), # (param_name , formula_instance , iterations)
    ]
# add the sweepSettings to the list

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [],
    "fixed_params_description_str": "",
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def policyTriggers_test33_nosweep():
# Curvi run:
# Formula: -hdi
# Param name           & Starting point & Max  & Min  & Curvi
# t_fert_cont_eff_time & 2034           & 2100 & 2018 & 2076.81717859103
# t_ind_equil_time     & 2034           & 2100 & 2018 & 2073.09706915164
# t_zero_pop_grow_time & 2034           & 2100 & 2018 & 2049.83898445364
# t_land_life_time     & 2034           & 2100 & 2018 & 2026.08829271848
# t_policy_year        & 2034           & 2100 & 2018 & 2034.32051122486
# t_fcaor_time         & 2034           & 2100 & 2018 & 2083.36491898977

# With:
# ier =   0 nfu =    13 nit =      0
# Time: ~2m on laptop


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("t_fert_cont_eff_time" , predef_formulas.OneValue(2076.81717859103   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_ind_equil_time"     , predef_formulas.OneValue(2073.09706915164   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_zero_pop_grow_time" , predef_formulas.OneValue(2049.83898445364    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_land_life_time"     , predef_formulas.OneValue(2026.08829271848   ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_policy_year"        , predef_formulas.OneValue(2034.32051122486   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_fcaor_time"         , predef_formulas.OneValue(2083.36491898977    ), 1),    # (param_name , formula_instance , iterations)
                                 ]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def policyTriggers_test32_nosweep():
# Curvi run:
# Formula: -hdi
# Param name           & Starting point & Max  & Min  & Curvi
# t_fert_cont_eff_time & 2018           & 2100 & 2018 & 2018
# t_ind_equil_time     & 2018           & 2100 & 2018 & 2018
# t_zero_pop_grow_time & 2018           & 2100 & 2018 & 2018
# t_land_life_time     & 2018           & 2100 & 2018 & 2018
# t_policy_year        & 2018           & 2100 & 2018 & 2018
# t_fcaor_time         & 2018           & 2100 & 2018 & 2018

# With:
# ier =   0 nfu =    13 nit =      0
# Time: ~2m on laptop


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("t_fert_cont_eff_time" , predef_formulas.OneValue(2018   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_ind_equil_time"     , predef_formulas.OneValue(2018   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_zero_pop_grow_time" , predef_formulas.OneValue(2018    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_land_life_time"     , predef_formulas.OneValue(2018   ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_policy_year"        , predef_formulas.OneValue(2018   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_fcaor_time"         , predef_formulas.OneValue(2018    ), 1),    # (param_name , formula_instance , iterations)
                                 ]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def policyTriggers_test31_nosweep():
# Curvi run:
# Formula: -hdi
# Param name           & Starting point & Max  & Min  & Curvi
# t_fert_cont_eff_time & 2050           & 2100 & 2018 & 2076.49542873992
# t_ind_equil_time     & 2050           & 2100 & 2018 & 2049.20235624306
# t_zero_pop_grow_time & 2050           & 2100 & 2018 & 2046.51075636435
# t_land_life_time     & 2050           & 2100 & 2018 & 2061.14818103240
# t_policy_year        & 2050           & 2100 & 2018 & 2049.72195968877
# t_fcaor_time         & 2050           & 2100 & 2018 & 2086.03299786679

# With:
# ier =   2 nfu =  1325 nit =     26
# Time: ~3h on laptop


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("t_fert_cont_eff_time" , predef_formulas.OneValue(2076.49542873992   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_ind_equil_time"     , predef_formulas.OneValue(2049.20235624306   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_zero_pop_grow_time" , predef_formulas.OneValue(2046.51075636435    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_land_life_time"     , predef_formulas.OneValue(2061.14818103240   ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_policy_year"        , predef_formulas.OneValue(2049.72195968877   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("t_fcaor_time"         , predef_formulas.OneValue(2086.03299786679    ), 1),    # (param_name , formula_instance , iterations)
                                 ]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def onlyMeasurableInitValsNoSweep5PercOptimizePop():
# Curvi run:
    # Optimum x0:
# Param name              & Default         & CurviVal5%       & Curvival5%/Default
# nr_resources_init       & 1000000000000.0 & 1049999932898.45 & 1.04999993289845
# pop2_init               & 700000000.0     & 734997926.769216 & 1.049997038241737
# industrial_capital_init & 210000000000.0  & 199500310116.404 & 0.9500014767447809
# pot_arable_land_tot     & 3200000000.0    & 3359996768.48028 & 1.0499989901500875
# pot_arable_land_init    & 2300000000.0    & 2185022565.87536 & 0.9500098112501565
# pop1_init               & 650000000.0     & 682495277.053796 & 1.049992733928917
# service_capital_init    & 144000000000.0  & 136865897154.419 & 0.9504576191279097
# arable_land_init        & 900000000.0     & 854999989.771129 & 0.9499999886345878
# land_fertility_init     & 600.0           & 574.830198743534 & 0.9580503312392232
# ppoll_in_1970           & 136000000.0     & 142799625.357823 & 1.0499972452781103
# agr_inp_init            & 5000000000.0    & 4765263042.21460 & 0.95305260844292
# urban_ind_land_init     & 8200000.0       & 7926983.79713496 & 0.9667053411140195
# pop3_init               & 190000000.0     & 190430747.405051 & 1.0022670916055316
# pop4_init               & 60000000.0      & 58481379.9505684 & 0.9746896658428067
# pers_pollution_init     & 25000000.0      & 25085149.6442214 & 1.003405985768856
# des_res_use_rt_DNRUR    & 4800000000.0    & 4753250667.76996 & 0.9902605557854084
# ind_out_in_1970         & 790000000000.0  & 790103354230.892 & 1.0001308281403696
# With:
#  ier =   2 nfu =  3271 nit =     23
#  fopt(pop) =    -0.43238705D+10


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"       , predef_formulas.IncreasingByDeltaNotInclusive(0.04999993289844995    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop2_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.04999703824173696    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("industrial_capital_init" , predef_formulas.IncreasingByDeltaNotInclusive(-0.04999852325521914    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_tot"     , predef_formulas.IncreasingByDeltaNotInclusive(0.04999899015008746    ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_init"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.04999018874984351   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop1_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.04999273392891701     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("service_capital_init"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.049542380872090286   ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("arable_land_init"        , predef_formulas.IncreasingByDeltaNotInclusive(-0.05000001136541221   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("land_fertility_init"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.04194966876077677   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("ppoll_in_1970"           , predef_formulas.IncreasingByDeltaNotInclusive(0.049997245278110336    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("agr_inp_init"            , predef_formulas.IncreasingByDeltaNotInclusive(-0.046947391557080054  ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("urban_ind_land_init"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.03329465888598049   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop3_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.0022670916055316237  ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop4_init"               , predef_formulas.IncreasingByDeltaNotInclusive(-0.025310334157193304    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pers_pollution_init"     , predef_formulas.IncreasingByDeltaNotInclusive(0.003405985768855979     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("des_res_use_rt_DNRUR"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.009739444214591608    ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("ind_out_in_1970"         , predef_formulas.IncreasingByDeltaNotInclusive(0.00013082814036957657 ), 1),     # (param_name , formula_instance , iterations)
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
def onlyMeasurableInitValsNoSweep3PercOptimizePop():
# Curvi run:
    # Optimum x0:
# Param name              & Default         & CurviVal3%       & Curvival3%/Default
# nr_resources_init       & 1000000000000.0 & 1029999969230.68 & 1.02999996923068
# pop2_init               & 700000000.0     & 720999966.773269 & 1.0299999525332415
# industrial_capital_init & 210000000000.0  & 203700100936.389 & 0.9700004806494714
# pot_arable_land_tot     & 3200000000.0    & 3295999683.65404 & 1.0299999011418874
# pot_arable_land_init    & 2300000000.0    & 2231000126.0827  & 0.9700000548185651
# pop1_init               & 650000000.0     & 669499907.842704 & 1.0299998582195447
# service_capital_init    & 144000000000.0  & 139680024201.879 & 0.9700001680686041
# arable_land_init        & 900000000.0     & 873000128.625531 & 0.9700001429172567
# land_fertility_init     & 600.0           & 582.003889499973 & 0.9700064824999549
# ppoll_in_1970           & 136000000.0     & 140079294.842117 & 1.0299948150155662
# agr_inp_init            & 5000000000.0    & 4854389902.22402 & 0.970877980444804
# urban_ind_land_init     & 8200000.0       & 7974013.07276953 & 0.9724406186304305
# pop3_init               & 190000000.0     & 194214755.894986 & 1.0221829257630843
# pop4_init               & 60000000.0      & 61646702.3275202 & 1.0274450387920033
# pers_pollution_init     & 25000000.0      & 25746881.1401298 & 1.029875245605192
# des_res_use_rt_DNRUR    & 4800000000.0    & 4908990166.58688 & 1.0227062847055999
# ind_out_in_1970         & 790000000000.0  & 790741017431.495 & 1.0009379967487277
# With:
#  ier =   2 nfu =  3271 nit =     23
#  fopt(pop) =    -0.43238705D+10


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"       , predef_formulas.IncreasingByDeltaNotInclusive(0.029999969230680046  ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop2_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.029999952533241503  ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("industrial_capital_init" , predef_formulas.IncreasingByDeltaNotInclusive(-0.02999951935052858   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_tot"     , predef_formulas.IncreasingByDeltaNotInclusive(0.02999990114188744   ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_init"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.029999945181434895 ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop1_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.02999985821954465    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("service_capital_init"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.02999983193139588   ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("arable_land_init"        , predef_formulas.IncreasingByDeltaNotInclusive(-0.02999985708274333  ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("land_fertility_init"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.029993517500045086 ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("ppoll_in_1970"           , predef_formulas.IncreasingByDeltaNotInclusive(0.029994815015566223   ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("agr_inp_init"            , predef_formulas.IncreasingByDeltaNotInclusive(-0.029122019555196    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("urban_ind_land_init"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.02755938136956948  ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop3_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.022182925763084338  ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop4_init"               , predef_formulas.IncreasingByDeltaNotInclusive(0.02744503879200333     ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pers_pollution_init"     , predef_formulas.IncreasingByDeltaNotInclusive(0.029875245605192058    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("des_res_use_rt_DNRUR"    , predef_formulas.IncreasingByDeltaNotInclusive(0.022706284705599877    ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("ind_out_in_1970"         , predef_formulas.IncreasingByDeltaNotInclusive(0.000937996748727743  ), 1),     # (param_name , formula_instance , iterations)
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
def relativeTop36ParamsNoSweep3PercentOptimizePop():
# Curvi run:
    # Optimum x0:
# Param name              & Default         & CurviVal3%            & Curvival3%/Default
# p_fioa_cons_const_1     & 0.43            & 0.442899987682584     & 1.0299999713548464
# p_ind_cap_out_ratio_1   & 3.0             & 3.08999990752248      & 1.02999996917416
# reproductive_lifetime   & 30.0            & 29.1000008660267      & 0.9700000288675567
# life_expect_norm        & 28.0            & 28.8399991624904      & 1.0299999700889428
# des_compl_fam_size_norm & 3.8             & 3.91399984153159      & 1.029999958297787
# p_avg_life_ind_cap_1    & 14.0            & 13.5800004005958      & 0.9700000286139857
# subsist_food_pc         & 230.0           & 223.100008793897      & 0.9700000382343348
# p_serv_cap_out_ratio_1  & 1.0             & 1.02999952398089      & 1.02999952398089
# max_tot_fert_norm       & 12.0            & 12.3599989076594      & 1.0299999089716165
# p_nr_res_use_fact_1     & 1.0             & 0.970000032740317     & 0.970000032740317
# nr_resources_init       & 1000000000000.0 & 1029999971346.01      & 1.02999997134601
# p_land_yield_fact_1     & 1.0             & 0.970037952266749     & 0.970037952266749
# pop2_init               & 700000000.0     & 720999683.82525       & 1.0299995483217859
# industrial_capital_init & 210000000000.0  & 203700454180.396      & 0.9700021627637905
# pot_arable_land_tot     & 3200000000.0    & 3199679898.37683      & 0.9998999682427594
# p_avg_life_serv_cap_1   & 20.0            & 19.4000013300908      & 0.97000006650454
# pot_arable_land_init    & 2300000000.0    & 2368999915.46405      & 1.029999963245239
# pop1_init               & 650000000.0     & 669493026.868808      & 1.0299892721058586
# ppoll_trans_del         & 20.0            & 20.5998524117882      & 1.0299926205894099
# land_fr_harvested       & 0.7             & 0.720999977562406     & 1.0299999679462943
# inherent_land_fert      & 600.0           & 617.999279020275      & 1.029998798367125
# lifet_perc_del          & 20.0            & 20.5996751832082      & 1.02998375916041
# service_capital_init    & 144000000000.0  & 139681021490.649      & 0.9700070936850624
# arable_land_init        & 900000000.0     & 926974042.126842      & 1.0299711579187134
# assim_half_life_1970    & 1.5             & 1.45500004311963      & 0.97000002874642
# land_fertility_init     & 600.0           & 617.268252440442      & 1.02878042073407
# p_ppoll_gen_fact_1      & 1.0             & 0.970000028664767     & 0.970000028664767
# avg_life_land_norm      & 1000.0          & 1029.998926769        & 1.029998926769
# fr_agr_inp_pers_mtl     & 0.001           & 0.0009700119654734652 & 0.9700119654734651
# agr_mtl_toxic_index     & 1.0             & 0.970088902055858     & 0.970088902055858
# ppoll_in_1970           & 136000000.0     & 140079994.330919      & 1.0299999583155808
# social_discount         & 0.07            & 0.06790001448018312   & 0.9700002068597589
# income_expect_avg_time  & 3.0             & 3.08996667172929      & 1.02998889057643
# social_adj_del          & 20.0            & 20.5999929544971      & 1.029999647724855
# hlth_serv_impact_del    & 20.0            & 19.4443365627337      & 0.972216828136685
# processing_loss         & 0.1             & 0.09727264397846881   & 0.9727264397846881

# With:
#  ier =   2 nfu = 21834 nit =     60
#  fopt(population) =    -0.12185403D+11


    sweep_params_settings_list = [ parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"      , predef_formulas.IncreasingByDeltaNotInclusive(0.029999971354846444    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"    , predef_formulas.IncreasingByDeltaNotInclusive(0.029999969174159924    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("reproductive_lifetime"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.029999971132443348    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("life_expect_norm"         , predef_formulas.IncreasingByDeltaNotInclusive(0.02999997008894284     ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("des_compl_fam_size_norm"  , predef_formulas.IncreasingByDeltaNotInclusive(0.02999995829778701     ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.02999997138601429     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("subsist_food_pc"          , predef_formulas.IncreasingByDeltaNotInclusive(-0.029999961765665217    ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_serv_cap_out_ratio_1"   , predef_formulas.IncreasingByDeltaNotInclusive(0.029999523980889897    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("max_tot_fert_norm"        , predef_formulas.IncreasingByDeltaNotInclusive(0.02999990897161653     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_nr_res_use_fact_1"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.029999967259683014    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"        , predef_formulas.IncreasingByDeltaNotInclusive(0.029999971346009957    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_land_yield_fact_1"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.02996204773325095     ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop2_init"                , predef_formulas.IncreasingByDeltaNotInclusive(0.029999548321785863    ), 1),          # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("industrial_capital_init"  , predef_formulas.IncreasingByDeltaNotInclusive(-0.029997837236209524     ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_tot"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.00010003175724060398   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_serv_cap_1"    , predef_formulas.IncreasingByDeltaNotInclusive(-0.02999993349546004      ), 1),       # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pot_arable_land_init"     , predef_formulas.IncreasingByDeltaNotInclusive(0.029999963245239014    ), 1),     # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("pop1_init"                , predef_formulas.IncreasingByDeltaNotInclusive(0.029989272105858555    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("ppoll_trans_del"          , predef_formulas.IncreasingByDeltaNotInclusive(0.02999262058940988     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("land_fr_harvested"        , predef_formulas.IncreasingByDeltaNotInclusive(0.029999967946294337    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("inherent_land_fert"       , predef_formulas.IncreasingByDeltaNotInclusive(0.029998798367125046    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("lifet_perc_del"           , predef_formulas.IncreasingByDeltaNotInclusive(0.029983759160409962    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("service_capital_init"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.029992906314937562    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("arable_land_init"         , predef_formulas.IncreasingByDeltaNotInclusive(0.02997115791871341     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("assim_half_life_1970"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.029999971253580004    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("land_fertility_init"      , predef_formulas.IncreasingByDeltaNotInclusive(0.028780420734070056    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("p_ppoll_gen_fact_1"       , predef_formulas.IncreasingByDeltaNotInclusive(-0.029999971335233022    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("avg_life_land_norm"       , predef_formulas.IncreasingByDeltaNotInclusive(0.029998926768999956    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("fr_agr_inp_pers_mtl"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.029988034526534868   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("agr_mtl_toxic_index"      , predef_formulas.IncreasingByDeltaNotInclusive(-0.02991109794414204    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("ppoll_in_1970"            , predef_formulas.IncreasingByDeltaNotInclusive(0.029999958315580777    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("social_discount"          , predef_formulas.IncreasingByDeltaNotInclusive(-0.02999979314024115    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("income_expect_avg_time"   , predef_formulas.IncreasingByDeltaNotInclusive(0.02998889057643006     ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("social_adj_del"           , predef_formulas.IncreasingByDeltaNotInclusive(0.029999647724854972    ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("hlth_serv_impact_del"     , predef_formulas.IncreasingByDeltaNotInclusive(-0.027783171863315026   ), 1),    # (param_name , formula_instance , iterations)
                                   parameter_sweep_settings.OrigParameterSweepSettings("processing_loss"          , predef_formulas.IncreasingByDeltaNotInclusive(-0.02727356021531191    ), 1),    # (param_name , formula_instance , iterations)
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
def relativeTop18ParamsNoSweep3PercentOptimizePop():
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
def relativeTop12ParamsNoSweep5PercentOptimizePopAndHWI():
#                            DEFAULT            Curvi Results        Curvi5%/def  Description
#     max_tot_fert_norm       & 12.0           & 11.4071116380366  & 0.95059263650305   & "Normal maximal total fertility"                                 \\
#     p_fioa_cons_const_1     & 0.43           & 0.451499899371272 & 1.0499997659797022 & "Default frac of industrial output allocated to consumption" \\
#     p_ind_cap_out_ratio_1   & 3.0            & 3.14847122749876  & 1.0494904091662534 & "Default industrial capital output ratio"                        \\
#     p_serv_cap_out_ratio_1  & 1.0            & 1.04226292625196  & 1.04226292625196   & "Default fraction of service sector output ratio"                \\
#     life_expect_norm        & 28.0           & 29.3138949698442  & 1.0469248203515786 & "Normal life expectancy"                                         \\
#     des_compl_fam_size_norm & 3.8            & 3.85710846315913  & 1.0150285429366133 & "Desired normal complete family size"                            \\
#     industrial_capital_init & 210000000000.0 & 199561334891.506  & 0.9502920709119334 & "Initial industrial investment"                       \\
#     p_land_yield_fact_1     & 1.0            & 0.99487613949118  & 0.99487613949118   & "Default land yield factor"                           \\
#     p_nr_res_use_fact_1     & 1.0            & 1.0456279056156   & 1.0456279056156    & "Default non-recoverable resource utilization factor" \\
#     reproductive_lifetime   & 30.0           & 28.6225928068215  & 0.95408642689405   & "Reproductive life time"                              \\
#     subsist_food_pc         & 230.0          & 220.202588706605  & 0.9574025595939348 & "Available per capita food"                           \\
#     p_avg_life_ind_cap_1    & 14.0           & 14.2937741358301  & 1.020983866845007  & "Default average life of industrial capital";         \\
# Curvi run:
    # Optimum x0:
#    (in the table above)
# With:
#  ier =   2 nfu =  1740 nit =     17
#  fopt(pop/1e10+hwi) =    -0.14702453D+01
# And +-1% of boundaries

    maxTotFertNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas . IncreasingByDeltaNotInclusive(-0.04940736349694996  ), 1) # (param_name , formula_instance , iterations)
    fioaConsConst1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas . IncreasingByDeltaNotInclusive( 0.04999976597970224  ), 1) # (param_name , formula_instance , iterations)
    indCapOutRatio1_sweepSettings  = parameter_sweep_settings     . OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas . IncreasingByDeltaNotInclusive( 0.04949040916625336  ), 1) # (param_name , formula_instance , iterations)
    servCapOutRatio1_sweepSettings  = parameter_sweep_settings    . OrigParameterSweepSettings("p_serv_cap_out_ratio_1"  , predef_formulas . IncreasingByDeltaNotInclusive( 0.04226292625196004  ), 1) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("life_expect_norm"        , predef_formulas . IncreasingByDeltaNotInclusive( 0.04692482035157863  ), 1) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings  = parameter_sweep_settings . OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas . IncreasingByDeltaNotInclusive( 0.015028542936613265 ), 1) # (param_name , formula_instance , iterations)
    indCapInit_sweepSettings  = parameter_sweep_settings          . OrigParameterSweepSettings("industrial_capital_init" , predef_formulas . IncreasingByDeltaNotInclusive(-0.04970792908806665  ), 1) # (param_name , formula_instance , iterations)
    landYieldFact1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(-0.005123860508819966 ), 1) # (param_name , formula_instance , iterations)
    nrResUseFact1_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("p_nr_res_use_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive( 0.04562790561559993  ), 1) # (param_name , formula_instance , iterations)
    reproLifetime_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas . IncreasingByDeltaNotInclusive(-0.04591357310595001  ), 1) # (param_name , formula_instance , iterations)
    subsistFoodPc_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("subsist_food_pc"         , predef_formulas . IncreasingByDeltaNotInclusive(-0.04259744040606517  ), 1) # (param_name , formula_instance , iterations)
    avgLifeIndCap1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas . IncreasingByDeltaNotInclusive( 0.020983866845007082 ), 1) # (param_name , formula_instance , iterations)
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
def relativeTop12ParamsNoSweep3PercentOptimizePopAndHWI():
#                            DEFAULT            Curvi Results        Curvi3%/def  Description
#     max_tot_fert_norm       & 12.0           & 12.3596702764035  & 1.029972523033625  & "Normal maximal total fertility"                                 \\
#     p_fioa_cons_const_1     & 0.43           & 0.442898026311551 & 1.029995410026863  & "Default frac of industrial output allocated to consumption" \\
#     p_ind_cap_out_ratio_1   & 3.0            & 3.08991285936927  & 1.02997095312309   & "Default industrial capital output ratio"                        \\
#     p_serv_cap_out_ratio_1  & 1.0            & 1.02992984922938  & 1.02992984922938   & "Default fraction of service sector output ratio"                \\
#     life_expect_norm        & 28.0           & 28.8399987213502  & 1.0299999543339358 & "Normal life expectancy"                                         \\
#     des_compl_fam_size_norm & 3.8            & 3.91379583273569  & 1.02994627177255   & "Desired normal complete family size"                            \\
#     industrial_capital_init & 210000000000.0 & 203751279614.653  & 0.9702441886412049 & "Initial industrial investment"                       \\
#     p_land_yield_fact_1     & 1.0            & 0.970035858720122 & 0.970035858720122  & "Default land yield factor"                           \\
#     p_nr_res_use_fact_1     & 1.0            & 0.970179653020971 & 0.970179653020971  & "Default non-recoverable resource utilization factor" \\
#     reproductive_lifetime   & 30.0           & 29.1019099670657  & 0.9700636655688567 & "Reproductive life time"                              \\
#     subsist_food_pc         & 230.0          & 223.100157593592  & 0.9700006851895304 & "Available per capita food"                           \\
#     p_avg_life_ind_cap_1    & 14.0           & 13.5800804459832  & 0.9700057461416571 & "Default average life of industrial capital";         \\
# Curvi run:
    # Optimum x0:
#    (in the table above)
# With:
#  ier =   2 nfu =  5182 nit =     68
#  fopt(pop/1e10+hwi) =    -0.14813551D+01
# And +-1% of boundaries

    maxTotFertNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas . IncreasingByDeltaNotInclusive( 0.029972523033624965 ), 1) # (param_name , formula_instance , iterations)
    fioaConsConst1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas . IncreasingByDeltaNotInclusive( 0.0299954100268629   ), 1) # (param_name , formula_instance , iterations)
    indCapOutRatio1_sweepSettings  = parameter_sweep_settings     . OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas . IncreasingByDeltaNotInclusive( 0.02997095312309006  ), 1) # (param_name , formula_instance , iterations)
    servCapOutRatio1_sweepSettings  = parameter_sweep_settings    . OrigParameterSweepSettings("p_serv_cap_out_ratio_1"  , predef_formulas . IncreasingByDeltaNotInclusive( 0.029929849229380023 ), 1) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("life_expect_norm"        , predef_formulas . IncreasingByDeltaNotInclusive( 0.029999954333935763 ), 1) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings  = parameter_sweep_settings . OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas . IncreasingByDeltaNotInclusive( 0.029946271772550048 ), 1) # (param_name , formula_instance , iterations)
    indCapInit_sweepSettings  = parameter_sweep_settings          . OrigParameterSweepSettings("industrial_capital_init" , predef_formulas . IncreasingByDeltaNotInclusive(-0.029755811358795126 ), 1) # (param_name , formula_instance , iterations)
    landYieldFact1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(-0.02996414127987801  ), 1) # (param_name , formula_instance , iterations)
    nrResUseFact1_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("p_nr_res_use_fact_1"     , predef_formulas . IncreasingByDeltaNotInclusive(-0.029820346979029022 ), 1) # (param_name , formula_instance , iterations)
    reproLifetime_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas . IncreasingByDeltaNotInclusive(-0.029936334431143297 ), 1) # (param_name , formula_instance , iterations)
    subsistFoodPc_sweepSettings  = parameter_sweep_settings       . OrigParameterSweepSettings("subsist_food_pc"         , predef_formulas . IncreasingByDeltaNotInclusive(-0.02999931481046958  ), 1) # (param_name , formula_instance , iterations)
    avgLifeIndCap1_sweepSettings  = parameter_sweep_settings      . OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas . IncreasingByDeltaNotInclusive(-0.029994253858342868 ), 1) # (param_name , formula_instance , iterations)
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
def relativeTop12ParamsNoSweep1PercentOptimizePop():
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
# ier =   0 nfu =   520 nit =      8
#  fopt(pop) =    -0.53767719D+10
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

def relativeTop12ParamsSweepOf2Params5PercentOptimizePop():
# We sweep the 2 params that differ from the single sensitivity calculations of Relative (presented in wp2)
# (similar to the "NoSweep" variant of this run, but sweeping 2 parameters)
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
    sweep_params_settings_list    = [
      parameter_sweep_settings      . OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas . DeltaBeforeAndAfter(0.05   ), 3), # (param_name , formula_instance , iterations)
      parameter_sweep_settings      . OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas . DeltaBeforeAndAfter(0.05), 3), # (param_name , formula_instance , iterations)
    ]
# add the sweepSettings to the list

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population","human_welfare_index"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [
        ("p_nr_res_use_fact_1"     ,0.949999988082543),
        ("max_tot_fert_norm"       ,12.5999994203700),
        ("p_fioa_cons_const_1"     ,0.448380420759870),
        ("p_ind_cap_out_ratio_1"   ,3.14999863042567),
        ("p_serv_cap_out_ratio_1"  ,1.04559432323735),
        ("life_expect_norm"        ,29.3999986573765),
        ("des_compl_fam_size_norm" ,3.98999981851597),
        ("industrial_capital_init" ,199499999088.315),
        ("reproductive_lifetime"   ,28.4999996571028),
        ("subsist_food_pc"         ,218.499997333924)
       ],
    "fixed_params_description_str": "10 parameters were perturbed to a fixed value. See description.",
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [2025,2050,2075] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def relativeTop12ParamsNoSweep5PercentOptimizePop():
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
# ier = 2 nfu = 1964 nit = 93 fopt(population) = -9985562545.07286
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
# ier = 2 nfu = 1964 nit = 93 fopt(population) = -9985562545.07286
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
def nrResourcesInitZXPOWLNoSweepOptimizePop():
    # Curvi results:
#  ier = 132 nfu =     1 nit =      0
#  Vector solucion =
#
#    1331113420897.75 ===> 1.33111342089775 ===> +33%
#
#  fopt(population) =    -0.43936607D+10


    nRResInit_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"      , predef_formulas.IncreasingByDeltaNotInclusive(0.33111342089775), 1) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [nRResInit_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
    "scens_to_run"               : [1], #The standard run corresponds to the first scenario
    "fixed_params"               : [], #We don't want to change any parameters
    "mo_file"                    : piecewiseMod_SysDyn_mo_path, # mo file with tabular modified (to allow out of tabular interpolation)
    "plot_std_run"               : True, #Choose to plot std run alognside this test results
    "extra_ticks"                : [] # extra years ticks for the plot(s)
    }
    setUpSweepsAndRun(**run_kwargs)
def nrResourcesInitCurviNoSweepOptimizePop():
    # Curvi results:
#  ier =   2 nfu =   370 nit =     14
#  Vector solucion =
#
#    1322956409277.25    ==> def/curvi = 1.32295640927725 = +32%
#
#  fopt(population) =    -0.43937738D+10

    nRResInit_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"      , predef_formulas.IncreasingByDeltaNotInclusive(0.32295640927725), 1) # (param_name , formula_instance , iterations)
# add the sweepSettings to the list
    sweep_params_settings_list    = [nRResInit_sweepSettings]

    run_kwargs = {
    "sweep_params_settings_list" : sweep_params_settings_list,
    "plot_vars"                  : ["population"],
    "stopTime"                   : 2500  ,# year to end the simulation (2100 for example)
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
        run_omc.runMosScript(output_mos_tobeExe_path)
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
