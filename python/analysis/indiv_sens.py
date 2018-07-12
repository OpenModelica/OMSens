# Std
import logging
import math  # for sqrt
import os  # for os.path
import re  # regular expressions
import unicodedata  # slugifying file names

import pandas  # dataframes

import filesystem.files_aux as files_aux
import plotting.plot_heatmap as heatmap_f

logger = logging.getLogger("--ParameterSensAnalysis--")  # this modules logger


def completeIndividualSensAnalysis(perturbed_simus_info, target_vars, percentage_perturbed, specific_year,
                                   rms_first_year, rms_last_year, std_run_csv_path, output_folder_analyses_path):
    # Create perturbed runs info list using the dict output form the mos script
    #  TODO: adapt this function when we stop using tuples inside the analyzer in favor of using proper objects to represent the info
    perturbed_csvs_path_and_info_pairs = perturbationAsTuplesFromDict(perturbed_simus_info)
    # Initialize result with paths
    sens_to_params_per_var = analysisPerParamPerturbedForEachVar(percentage_perturbed,
                                                                 perturbed_csvs_path_and_info_pairs,
                                                                 rms_first_year, rms_last_year, specific_year,
                                                                 std_run_csv_path, target_vars)
    # Complete sensitivity information for each variable
    vars_sens_infos_paths = sensitivitiesInformationPathsPerVariable(output_folder_analyses_path, percentage_perturbed,
                                                                     rms_first_year, rms_last_year,
                                                                     sens_to_params_per_var, specific_year, target_vars)
    # Sensitivities matrices of "param/var" per method
    sens_matrices_dfs_dict = generateSensMatricesPerMethod(output_folder_analyses_path, rms_first_year,
                                                           rms_last_year,
                                                           sens_to_params_per_var)
    sens_matrices_folder_path = makeFolderForMethodsMatricesFiles(output_folder_analyses_path)
    sens_matrices_paths = writeMethodsMatricesToFiles(sens_matrices_dfs_dict["Relative"], sens_matrices_dfs_dict["RMS"],
                                                      sens_matrices_folder_path)
    # Create folder for heatmapas
    sens_heatmaps_folder_path = makeFolderForMethodsHeatmapFiles(output_folder_analyses_path)
    # Iterate indices creating a Heatmap for each and saving their paths
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
        "sens_matrices": sens_matrices_paths,
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


def perturbationAsTuplesFromDict(perturbed_simus_info):
    perturbed_csvs_path_and_info_pairs = []
    for param_name in perturbed_simus_info:
        # Gather simulation info from mos
        perturbed_run_info = perturbed_simus_info[param_name]
        simu_file_path = perturbed_run_info["simu_file_path"]
        std_val = perturbed_run_info["std_val"]
        perturbed_val = perturbed_run_info["perturbed_val"]
        # Create tuple from using info
        perturb_tuple = (simu_file_path, (param_name, std_val, perturbed_val))
        # Add tuple to list
        perturbed_csvs_path_and_info_pairs.append(perturb_tuple)
    return perturbed_csvs_path_and_info_pairs


def generateSensMatricesPerMethod(output_folder_analyses_path, rms_first_year, rms_last_year,
                                  sens_to_params_per_var):
    methods_records_dict = generateMatrixRecordsForEachSensitivityMethod(rms_first_year, rms_last_year,
                                                                         sens_to_params_per_var)
    df_rel_matrix_trans, df_rms_matrix_trans = methodsDataframesFromRecordsDict(methods_records_dict)
    # Write the matrices to file
    sens_matrices_dfs_dict = {
        "Relative": df_rel_matrix_trans,
        "RMS": df_rms_matrix_trans,
    }
    return sens_matrices_dfs_dict


def makeFolderForMethodsMatricesFiles(output_folder_analyses_path):
    # Create folder for matrices per method
    sens_matrices_folder_name = "sens_matrices_per_method"
    sens_matrices_folder_path = os.path.join(output_folder_analyses_path, sens_matrices_folder_name)
    files_aux.makeFolderWithPath(sens_matrices_folder_path)
    return sens_matrices_folder_path


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


def writeMethodsMatricesToFiles(df_rel_matrix_trans, df_rms_matrix_trans, sens_matrices_folder_path):
    # Write the relative method matrix to file
    rel_mat_name = "relative_method_matrix.csv"
    rel_mat_path = os.path.join(sens_matrices_folder_path, rel_mat_name)
    df_rel_matrix_trans.to_csv(rel_mat_path)
    # Write the RMS method matrix to file
    rms_mat_name = "rms_method_matrix.csv"
    rms_mat_path = os.path.join(sens_matrices_folder_path, rms_mat_name)
    df_rms_matrix_trans.to_csv(rms_mat_path)
    return {
        "rel": rel_mat_path,
        "rms": rms_mat_path,
    }


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


def analysisPerParamPerturbedForEachVar(percentage_perturbed, perturbed_csvs_path_and_info_pairs, rms_first_year,
                                        rms_last_year, specific_year, std_run_csv_path, target_vars):
    # Initialize dict with rows for each variable. Each row will correspond to the values of said variable for a
    #   respective run from each respective parameter perturbed
    sens_to_params_per_var = {var_name: {} for var_name in target_vars}
    # Read standard run output that we will use as default output
    df_std_run = pandas.read_csv(std_run_csv_path, index_col=0)
    # Iterate simulations for each parameter perturbed in isolation
    for param_csv_path, param_info in perturbed_csvs_path_and_info_pairs:
        analyzeParamResultsForEachVar(df_std_run, param_csv_path, param_info, percentage_perturbed, rms_first_year,
                                      rms_last_year, specific_year, target_vars, sens_to_params_per_var)
    return sens_to_params_per_var


def analyzeParamResultsForEachVar(df_std_run, param_csv_path, param_info, percentage_perturbed, rms_first_year,
                                  rms_last_year, specific_year, target_vars, sens_to_params_per_var):
    # Read perturbed parameter csv
    df_param_perturbed = pandas.read_csv(param_csv_path, index_col=0)
    # Get param info such as name, default value, etc
    param_name, param_default, param_new_value = extractParamInfo(param_info)
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


def extractParamInfo(param_info):
    param_name = param_info[0]
    param_default = param_info[1]
    param_new_value = param_info[2]
    return param_name, param_default, param_new_value


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
