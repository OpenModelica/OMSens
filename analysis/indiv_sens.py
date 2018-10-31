# Std
import logging
import math  # for sqrt
import os  # for os.path
import re  # regular expressions
import unicodedata  # slugifying file names

import pandas  # dataframes

import filesystem.files_aux as files_aux
import plotting.plot_heatmap as heatmap_f
import modelica_interface.build_model as build_model
import running.simulation_run_info as simu_run_info

logger = logging.getLogger("--ParameterSensAnalysis--")  # this modules logger


class ParametersIsolatedPerturbator():
    def __init__(self, model_name, model_file_path, start_time, stop_time, parameters, perc_perturb, build_folder_path):
        # Save args
        self.model_name = model_name
        self.model_file_path = model_file_path
        self.start_time = start_time
        self.stop_time = stop_time
        self.parameters = parameters
        self.perc_perturb = perc_perturb
        # Initialize builder
        self.model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)
        # Build model
        self.compiled_model = self.model_builder.buildToFolderPath(build_folder_path)
        # Get the default values for the params to perturb using the compiled model
        self.params_defaults = self.defaultValuesForParamsToPerturb(self.compiled_model)
        # Calculate the values per param
        self.values_per_param = perturbedValuePerParam(self.params_defaults, self.parameters, self.perc_perturb)

    def runSimulations(self,dest_folder_path):
        # Make folder for runs
        runs_folder_name = "runs"
        runs_folder_path = os.path.join(dest_folder_path, runs_folder_name)
        files_aux.makeFolderWithPath(runs_folder_path)
        # Run STD run
        std_run_name = "std_run.csv"
        std_run_path = os.path.join(runs_folder_path, std_run_name)
        flags = "-noEventEmit"
        std_run_results = self.compiled_model.simulate(std_run_path, optional_flags=flags)
        # Make dir for perturbed runs
        perturbed_runs_folder_name = "perturbed"
        perturbed_runs_folder_path = os.path.join(runs_folder_path, perturbed_runs_folder_name)
        files_aux.makeFolderWithPath(perturbed_runs_folder_path)
        # Run the simulations for each parameter perturbed in isolation
        runs_per_parameter = {}
        i = 0
        for param_name in self.values_per_param:
            # Get param info for its run
            param_default_val = self.params_defaults[param_name]
            param_perturbed_val = self.values_per_param[param_name]
            # Perturb the parameter
            self.compiled_model.setParameterStartValue(param_name, param_perturbed_val)
            # Run the simulation
            simu_csv_name = "run_{0}.csv".format(i)
            simu_csv_path = os.path.join(perturbed_runs_folder_path, simu_csv_name)
            flags = "-noEventEmit"
            simu_results = self.compiled_model.simulate(simu_csv_path, optional_flags=flags)
            # Return the parameter to its original value
            self.compiled_model.setParameterStartValue(param_name, param_default_val)
            # Save the simulation results for this perturbed parameter
            perturbed_param_info = simu_run_info.PerturbedParameterInfo(param_name, param_default_val,
                                                                        param_perturbed_val)
            iter_results = OneParameterPerturbedResults(simu_results, perturbed_param_info)
            runs_per_parameter[param_name] = iter_results
            i=i+1
        # Prepare the results instance
        isolated_perturbations_results = IsolatedPerturbationsResults(self.model_name, std_run_results,
                                                                      runs_per_parameter)
        return isolated_perturbations_results


    # Auxs
    def defaultValuesForParamsToPerturb(self, compiled_model):
        # Using the compiled model, ask for the default value of each one
        params_defaults = {}
        for p in self.parameters:
            p_def_val = compiled_model.defaultParameterValue(p)
            params_defaults[p] = p_def_val
        return params_defaults


class IsolatedPerturbationsResults():
    def __init__(self,model_name, std_run, runs_per_parameter):
        self.model_name = model_name
        self.std_run = std_run
        self.runs_per_parameter = runs_per_parameter

class OneParameterPerturbedResults():
    def __init__(self, simu_results, pert_param_info):
        self.simu_results = simu_results
        self.pert_param_info = pert_param_info

def perturbedValuePerParam(params_defaults, parameters, perc_perturb):
    value_per_param = {}
    for param_name in parameters:
        # Disaggregate param info
        def_value = params_defaults[param_name]
        perturbed_val = def_value * (1 + perc_perturb / 100)
        value_per_param[param_name] = perturbed_val
    return value_per_param


def completeIndividualSensAnalysis(isolated_perturbations_results, target_vars, percentage_perturbed, specific_year,
                                   rms_first_year, rms_last_year, output_folder_analyses_path):
    # Create perturbed runs info list using the dict output form the mos script
    #  TODO: adapt this function when we stop using tuples inside the analyzer in favor of using proper objects to represent the info
    perturbed_csvs_path_and_info_pairs = perturbationAsTuplesFromDict(isolated_perturbations_results)
    # Initialize result with paths
    sens_to_params_per_var = analysisPerParamPerturbedForEachVar(isolated_perturbations_results,percentage_perturbed,
                                                                 rms_first_year, rms_last_year, specific_year,
                                                                 target_vars)
    # Complete sensitivity information for each variable
    vars_sens_infos_paths = sensitivitiesInformationPathsPerVariable(output_folder_analyses_path, percentage_perturbed,
                                                                     rms_first_year, rms_last_year,
                                                                     sens_to_params_per_var, specific_year, target_vars)
    # Per sens method analysis
    sens_matrices_dfs_dict = generateSensMatricesPerMethod(rms_first_year, rms_last_year, sens_to_params_per_var)
    # Create folder for heatmapas
    sens_heatmaps_folder_path = makeFolderForMethodsHeatmapFiles(output_folder_analyses_path)
    # Iterate indices matrices creating a Heatmap for each
    heatmaps_files_paths_per_method = {}
    for method, df_matrix in sens_matrices_dfs_dict.items():
        # Create heatmap instance
        heatmap = heatmap_f.Heatmap(df_matrix)
        # Create folder for heatmaps of this method
        method_heatmap_folder_name = method
        method_heatmap_folder_path = os.path.join(sens_heatmaps_folder_path, method_heatmap_folder_name)
        files_aux.makeFolderWithPath(method_heatmap_folder_path)
        # Plot heatmap into folder path
        method_heatmap_files_paths = heatmap.plotInFolder(method_heatmap_folder_path)
        # Add this method's heatmaps to the dict
        heatmaps_files_paths_per_method[method] = method_heatmap_files_paths

    # Add paths to dict with paths
    analysis_files_paths = {
        "vars_sens_info": vars_sens_infos_paths,
        "heatmaps": heatmaps_files_paths_per_method,
    }
    # Add dfs to  dict with dfs
    analysis_dfs = {
        "sens_matrices": sens_matrices_dfs_dict,
    }
    # Make main dict with all sub-dicts
    analysis_results = {
        "paths": analysis_files_paths,
        "dfs": analysis_dfs,
    }
    return analysis_results


def perturbationAsTuplesFromDict(isolated_perturbations_results):
    runs_per_parameter = isolated_perturbations_results.runs_per_parameter
    perturbed_csvs_path_and_info_pairs = []
    for param_name in runs_per_parameter:
        # Gather simulation info from mos
        pert_run_info = runs_per_parameter[param_name]
        simu_file_path = pert_run_info.simu_results.output_path
        std_val = pert_run_info.pert_param_info.default_val
        perturbed_val = pert_run_info.pert_param_info.new_val
        # Create tuple from using info
        perturb_tuple = (simu_file_path, (param_name, std_val, perturbed_val))
        # Add tuple to list
        perturbed_csvs_path_and_info_pairs.append(perturb_tuple)
    return perturbed_csvs_path_and_info_pairs


def generateSensMatricesPerMethod(rms_first_year, rms_last_year,
                                  sens_to_params_per_var):
    methods_records_dict = generateMatrixRecordsForEachSensitivityMethod(rms_first_year, rms_last_year,
                                                                         sens_to_params_per_var)
    df_rel_matrix_trans, df_rms_matrix_trans = methodsDataframesFromRecordsDict(methods_records_dict)
    # Return dict with the indices respective matrices
    sens_matrices_dfs_dict = {
        "Relative": df_rel_matrix_trans,
        "RMS": df_rms_matrix_trans,
    }
    return sens_matrices_dfs_dict

def makeFolderForMethodsHeatmapFiles(output_folder_analyses_path):
    # Create folder for matrices per method
    sens_matrices_folder_name = "heatmaps"
    sens_matrices_folder_path = os.path.join(output_folder_analyses_path, sens_matrices_folder_name)
    files_aux.makeFolderWithPath(sens_matrices_folder_path)
    return sens_matrices_folder_path


def generateMatrixRecordsForEachSensitivityMethod(rms_first_year, rms_last_year, sens_to_params_per_var):
    # Initialize the dict that will have the records (rows of the matrix) for each method
    methods_records_dict = {"Rel": [], "RMS": []}
    # Generate the records (row of the matrix) from the sensitivities of the params vs vars
    for var_name in sens_to_params_per_var:
        rel_method_record, rms_method_record = methodsRecordsForVariable(rms_first_year, rms_last_year,
                                                                         sens_to_params_per_var, var_name)
        # Add the records from the methods to their respective keys in the final dict
        methods_records_dict["Rel"].append(rel_method_record)
        methods_records_dict["RMS"].append(rms_method_record)
    return methods_records_dict


def methodsRecordsForVariable(rms_first_year, rms_last_year, sens_to_params_per_var, var_name):
    # Get the sens info associated with this variable
    params_sens_to_var = sens_to_params_per_var[var_name]
    # Initialize the records for this variable. Each record corresponds to a variable and has information of its
    #   sensitivity to each parameter according to a given sensitivity method
    rel_method_record = {"parameter/variable": var_name}
    rms_method_record = {"parameter/variable": var_name}
    # Iterate the parameters adding for each one its information for each sensitivity method
    for param_name in params_sens_to_var:
        addParamsMethodsValsToVarsRecords(param_name, params_sens_to_var, rel_method_record, rms_first_year,
                                          rms_last_year, rms_method_record)
    return rel_method_record, rms_method_record


def addParamsMethodsValsToVarsRecords(param_name, params_sens_to_var, rel_method_record, rms_first_year, rms_last_year,
                                      rms_method_record):
    var_vs_param_sens = params_sens_to_var[param_name]
    # Get relative method info
    rel_method_val = var_vs_param_sens["(new-std)/std"]
    # Add it to its respective record
    rel_method_record[param_name] = rel_method_val
    # Get RMS method info
    rms_method_val = var_vs_param_sens["root_mean_square_{0}_to_{1}".format(rms_first_year, rms_last_year)]
    # Add it to its respective record
    rms_method_record[param_name] = rms_method_val


def methodsDataframesFromRecordsDict(methods_records_dict):
    # Generate dataframes from the matrices
    df_rel_matrix = pandas.DataFrame.from_records(methods_records_dict["Rel"], index="parameter/variable")
    df_rms_matrix = pandas.DataFrame.from_records(methods_records_dict["RMS"], index="parameter/variable")
    # Transpose the matrices so we have the parameters as rows and the variables as columns
    df_rel_matrix_trans = df_rel_matrix.transpose()
    df_rms_matrix_trans = df_rms_matrix.transpose()
    return df_rel_matrix_trans, df_rms_matrix_trans

def sensitivitiesInformationPathsPerVariable(output_folder_analyses_path, percentage_perturbed, rms_first_year,
                                             rms_last_year, sens_to_params_per_var, specific_year, target_vars):
    # Create folder for complete sensitivity info per var
    vars_sens_info_folder_name = "vars_sens_info"
    vars_sens_info_folder_path = os.path.join(output_folder_analyses_path, vars_sens_info_folder_name)
    files_aux.makeFolderWithPath(vars_sens_info_folder_path)
    # Run infos paths, a dict with vars as keys and values the paths to their respective sens info
    vars_sens_infos_paths = writeRunInfosAndReturnThePaths(vars_sens_info_folder_path, percentage_perturbed,
                                                           rms_first_year,
                                                           rms_last_year, specific_year, target_vars,
                                                           sens_to_params_per_var)
    return vars_sens_infos_paths


def analysisPerParamPerturbedForEachVar(isolated_perturbations_results, percentage_perturbed, rms_first_year,
                                        rms_last_year, specific_year, target_vars):
    # Initialize dict with rows for each variable. Each row will correspond to the values of said variable for a
    #   respective run from each respective parameter perturbed
    sens_to_params_per_var = {var_name: {} for var_name in target_vars}
    # Read standard run output that we will use as default output
    std_run_csv_path = isolated_perturbations_results.std_run.output_path
    df_std_run = pandas.read_csv(std_run_csv_path, index_col=0)
    # Iterate simulations for each parameter perturbed in isolation
    perturbed_runs = isolated_perturbations_results.runs_per_parameter
    for param_name in perturbed_runs:
        pert_run_info = perturbed_runs[param_name]
        analyzeParamResultsForEachVar(df_std_run, pert_run_info, percentage_perturbed, rms_first_year,
                                      rms_last_year, specific_year, target_vars, sens_to_params_per_var)
    return sens_to_params_per_var


def analyzeParamResultsForEachVar(df_std_run, pert_run_info, percentage_perturbed, rms_first_year,
                                  rms_last_year, specific_year, target_vars, sens_to_params_per_var):
    # Read perturbed parameter csv
    param_csv_path = pert_run_info.simu_results.output_path
    df_param_perturbed = pandas.read_csv(param_csv_path, index_col=0)
    # Get param info such as name, default value, etc
    param_name       = pert_run_info.pert_param_info.name
    param_default    = pert_run_info.pert_param_info.default_val
    param_new_value  = pert_run_info.pert_param_info.new_val
    # Iterate variables getting the values in the perturbed param csv
    for target_var in target_vars:
        analyzeVarFromPerturbedParamResults(df_param_perturbed, df_std_run, param_csv_path, param_default,
                                            param_name, param_new_value, percentage_perturbed, rms_first_year,
                                            rms_last_year, specific_year, target_var, sens_to_params_per_var)


def analyzeVarFromPerturbedParamResults(df_param_perturbed, df_std_run, param_csv_path, param_default, param_name,
                                        param_new_value, percentage_perturbed, rms_first_year, rms_last_year,
                                        specific_year, target_var, sens_to_params_per_var):
    var_analysis_dict = varAnalysisForPerturbedParam(df_std_run, df_param_perturbed, target_var, specific_year,
                                                     rms_first_year, rms_last_year)
    sens_file_row_dict = rowDictFromParamVarSensAnal(param_name, param_default, param_new_value,
                                                     percentage_perturbed, specific_year, rms_first_year,
                                                     rms_last_year, var_analysis_dict, param_csv_path)
    # Get the sensitivities up to now corresponding to this variable
    var_sens_per_param = sens_to_params_per_var[target_var]
    # Add the ones for this param
    var_sens_per_param[param_name] = sens_file_row_dict


def writeRunInfosAndReturnThePaths(output_folder_analyses_path, percentage_perturbed, rms_first_year, rms_last_year,
                                   specific_year, target_vars, sens_to_params_per_var):
    run_infos_paths = {}
    # Set the columns order of the sensitivity analysis csv
    columns_order = varSensAnalysisInfodefaultColsOrder(percentage_perturbed, specific_year, rms_first_year,
                                                        rms_last_year)
    # Create a df for each var using its rows
    for target_var in target_vars:
        df_run_info = dataFrameWithSensAnalysisForVar(sens_to_params_per_var, target_var, columns_order)
        # Write sensitivity df to csv file
        run_info_path = dfPathFromFolderPathAndVarName(output_folder_analyses_path, target_var)
        df_run_info.to_csv(run_info_path, index=False)
        # Add file path to run infos paths dict
        run_infos_paths[target_var] = run_info_path
    return run_infos_paths


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value)
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value


def rootMeanSquareForVar(df_std_run, df_param_perturbed, rms_first_year, rms_last_year, target_var):
    # Get the columns from year to year indicated for std run and perturbed param run
    col_subyrs_std = df_std_run[target_var].loc[rms_first_year:rms_last_year]
    col_subyrs_perturbed = df_param_perturbed[target_var].loc[rms_first_year:rms_last_year]
    # Assert that both columns have the same number of rows
    raiseErrorIfDifferentLengthsInDFs(df_std_run, df_param_perturbed)
    # Calculate root mean square from both columns
    diff = col_subyrs_std - col_subyrs_perturbed
    diff_squared = diff ** 2
    mean_diff_squared = diff_squared.mean()
    rms = math.sqrt(mean_diff_squared)
    return rms

def varAnalysisForPerturbedParam(df_std_run, df_param_perturbed, target_var, specific_year, rms_first_year,
                                 rms_last_year):
    # Get values for variable from standard run and perturbed run outputs and an specific year
    var_std_value_for_year = df_std_run[target_var][specific_year]
    var_new_value_for_year = df_param_perturbed[target_var][specific_year]
    # Calculate sensitivity methods for an specific year
    std_div_new = var_std_value_for_year / var_new_value_for_year
    perturbation_proportion = (var_new_value_for_year - var_std_value_for_year) / var_std_value_for_year
    perturbation_proportion_abs = abs(perturbation_proportion)
    # Calculate sensitivity methods for the whole run
    rootMeanSquare = rootMeanSquareForVar(df_std_run, df_param_perturbed, rms_first_year, rms_last_year, target_var)

    var_analysis_dict = {
        "var_std_value_for_year": var_std_value_for_year,
        "var_new_value_for_year": var_new_value_for_year,
        "std_div_new": std_div_new,
        "perturbation_proportion": perturbation_proportion,
        "perturbation_proportion_abs": perturbation_proportion_abs,
        "rootMeanSquare": rootMeanSquare,
    }
    return var_analysis_dict


def varSensAnalysisInfodefaultColsOrder(percentage_perturbed, specific_year, rms_first_year, rms_last_year):
    columns_order = [
        "parameter",
        "parameter_default",
        "parameter_perturbed_{0}_percent".format(percentage_perturbed),
        "std_at_t_{0}".format(specific_year),
        "new_at_t_{0}".format(specific_year),
        "std/new",
        "(new-std)/std",
        "ABS((new-std)/std)",
        "root_mean_square_{0}_to_{1}".format(rms_first_year, rms_last_year),
        "perturbed_param_csv_path",
    ]
    return columns_order


def dataFrameWithSensAnalysisForVar(sens_to_params_per_var, target_var, columns_order):
    # Get sensitivities corresponding to this variable
    var_sens_per_param = sens_to_params_per_var[target_var]
    # Make records from the sens to be used in the dataframe
    var_sens_per_param_records = [v for k, v in var_sens_per_param.items()]
    # Create dataframe from the records
    df_run_info = pandas.DataFrame.from_records(var_sens_per_param_records, columns=columns_order)
    # Sort by diff column so we get the "most different" up top
    df_run_info = df_run_info.sort_values(by="ABS((new-std)/std)", ascending=False)
    return df_run_info

def dfPathFromFolderPathAndVarName(output_folder_analyses_path, target_var):
    var_name_slugified = slugify(target_var)
    var_sens_csv_file_name = "sens_{0}.csv".format(var_name_slugified)
    output_analysis_path = os.path.join(output_folder_analyses_path, var_sens_csv_file_name)
    return output_analysis_path


def rowDictFromParamVarSensAnal(param_name, param_default, param_new_value, percentage_perturbed, specific_year,
                                rms_first_year, rms_last_year, var_analysis_dict, param_csv_path):
    sens_file_row_dict = {
        "parameter": param_name,
        "parameter_default": param_default,
        "parameter_perturbed_{0}_percent".format(percentage_perturbed): param_new_value,
        "std_at_t_{0}".format(specific_year): var_analysis_dict["var_std_value_for_year"],
        "new_at_t_{0}".format(specific_year): var_analysis_dict["var_new_value_for_year"],
        "std/new": var_analysis_dict["std_div_new"],
        "(new-std)/std": var_analysis_dict["perturbation_proportion"],
        "ABS((new-std)/std)": var_analysis_dict["perturbation_proportion_abs"],
        "root_mean_square_{0}_to_{1}".format(rms_first_year, rms_last_year): var_analysis_dict["rootMeanSquare"],
        "perturbed_param_csv_path": param_csv_path,
    }
    return sens_file_row_dict


def raiseErrorIfDifferentLengthsInDFs(df_1, df_2):
    # Get both dfs shapes
    nrows_1, ncols_1 = df_1.shape
    nrows_2, ncols_2 = df_2.shape
    # Test both dimensions separately
    error_str_skeleton = "One simulation result has {0} {1} while the other has {2}"
    if not nrows_1 == nrows_2:
        raise InvalidSimulationResultsException(error_str_skeleton.format(nrows_1, "rows", nrows_2))
    if not ncols_1 == ncols_2:
        raise InvalidSimulationResultsException(error_str_skeleton.format(ncols_1, "columns", ncols_2))
    return 0


# Exceptions and the like
class InvalidSimulationResultsException(Exception):
    pass
