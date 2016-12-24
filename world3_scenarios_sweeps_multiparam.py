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
    test12fromTop12RelativeWP2()

### WP 3 tests ####
def test12fromTop12RelativeWP2OneUpOneDown():

    # Declare each parameter settings separately and then add them to the list manually
# Con one up one down
    indCapInit_sweepSettings          = parameter_sweep_settings.OrigParameterSweepSettings("industrial_capital_init" , predef_formulas.DeltaOneUpAndOneDown(0.01) , 2) # (param_name , formula_instance , iterations)
# Orig
    landYieldFact_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_land_yield_fact_1"     , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    nRResUseFact_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("p_nr_res_use_fact_1"     , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    reproLifet_sweepSettings          = parameter_sweep_settings.OrigParameterSweepSettings("reproductive_lifetime"   , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    subsistFood_sweepSettings         = parameter_sweep_settings.OrigParameterSweepSettings("subsist_food_pc"         , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    avgLifeIndCap_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_avg_life_ind_cap_1"    , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    maxTotFertNorm_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("max_tot_fert_norm"       , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    fioaConsConst_sweepSettings       = parameter_sweep_settings.OrigParameterSweepSettings("p_fioa_cons_const_1"     , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    indCapOutRat_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("p_ind_cap_out_ratio_1"   , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    servCapOutRatio_sweepSettings     = parameter_sweep_settings.OrigParameterSweepSettings("p_serv_cap_out_ratio_1"  , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    lifeExpectNorm_sweepSettings      = parameter_sweep_settings.OrigParameterSweepSettings("life_expect_norm"        , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
    desComplFamSizeNorm_sweepSettings = parameter_sweep_settings.OrigParameterSweepSettings("des_compl_fam_size_norm" , predef_formulas.DeltaOneUpAndOneDown(0.01) , 5) # (param_name , formula_instance , iterations)
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
    nrRes_sweepSettings        = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init"      , predef_formulas.DeltaBeforeAndAfter(0.1)  , 5) # (param_name , formula_instance , iterations)
    sweep_params_settings_list = [ inExAvgTim_sweepSettings, indCapOutRat_sweepSettings,nrRes_sweepSettings]

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
    nRRes_sweepSettings   = parameter_sweep_settings.OrigParameterSweepSettings("nr_resources_init" , predef_formulas.DeltaBeforeAndAfter(0.1) , 10) # (param_name , formula_instance , iterations)
    sweep_params_settings_list = [ nRRes_sweepSettings ]
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

def setUpSweepsAndRun(sweep_params_settings_list,fixed_params,plot_vars,stopTime,scens_to_run,mo_file,plot_std_run,fixed_params_description_str=False):
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
        plot_csv.plotVarsFromIterationsInfo(plot_vars,model_name,iterationsInfo_list,plots_folder_path,plot_std_run,fixed_params_description_str)
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
