# Std
import os  # for os.path
import math  # for sqrt
import pandas  # dataframes
import unicodedata  # slugifying file names
import re  # regular expressions
import logging

logger = logging.getLogger("--ParameterSensAnalysis--")  # this modules logger


def completeIndividualSensAnalysis(perturbed_csvs_path_and_info_pairs, target_vars, percentage_perturbed, specific_year,
                                   rms_first_year, rms_last_year, std_run_csv_path, output_folder_analyses_path):
    # Initialize result with paths
    analysis_files_paths = {}
    # Initialize dict with rows for each variable. Each row will correspond to the values of said variable for a
    #   respective run from each respective parameter perturbed
    vars_rows_dicts = {var_name: [] for var_name in target_vars}
    # Read standard run output that we will use as default output
    df_std_run = pandas.read_csv(std_run_csv_path, index_col=0)
    # Iterate simulations for each parameter perturbed in isolation
    for param_csv_path, param_info in perturbed_csvs_path_and_info_pairs:
        # Read perturbed parameter csv
        df_param_perturbed = pandas.read_csv(param_csv_path, index_col=0)
        # Get param info such as name, default value, etc
        param_name, param_default, param_new_value = extractParamInfo(param_info)
        # Iterate variables getting the values in the perturbed param csv
        for target_var in target_vars:
            var_analysis_dict = varAnalysisForPerturbedParam(df_std_run, df_param_perturbed, target_var, specific_year,
                                                             rms_first_year, rms_last_year)
            sens_file_row_dict = rowDictFromParamVarSensAnal(param_name, param_default, param_new_value,
                                                             percentage_perturbed, specific_year, rms_first_year,
                                                             rms_last_year, var_analysis_dict, param_csv_path)
            # Add this row to the rows of this respective variable
            var_rows = vars_rows_dicts[target_var]
            var_rows.append(sens_file_row_dict)
    # Initialize dict with run infos paths, it will have one key per var
    run_infos_paths = writeRunInfosAndReturnThePaths(output_folder_analyses_path, percentage_perturbed, rms_first_year,
                                                     rms_last_year, specific_year, target_vars, vars_rows_dicts)
    # Add run infos paths to main dict with paths
    analysis_files_paths["run_infos_per_var"] = run_infos_paths
    return analysis_files_paths


def writeRunInfosAndReturnThePaths(output_folder_analyses_path, percentage_perturbed, rms_first_year, rms_last_year,
                                   specific_year, target_vars, vars_rows_dicts):
    run_infos_paths = {}
    # Set the columns order of the sensitivity analysis csv
    columns_order = defaultColsOrder(percentage_perturbed, specific_year, rms_first_year, rms_last_year)
    # Create a df for each var using its rows
    for target_var in target_vars:
        df_run_info = dataFrameWithSensAnalysisForVar(vars_rows_dicts, target_var, columns_order)
        # Write sensitivity df to csv file
        run_info_path = writeRunInfoFromDF(df_run_info, target_var, output_folder_analyses_path)
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
    mean_diff_squared = sum(diff_squared) / len(diff_squared)
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


def defaultColsOrder(percentage_perturbed, specific_year, rms_first_year, rms_last_year):
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


def dataFrameWithSensAnalysisForVar(vars_rows_dicts, target_var, columns_order):
    var_rows = vars_rows_dicts[target_var]
    df_run_info = pandas.DataFrame.from_records(var_rows, columns=columns_order)
    # Sort by diff column so we get the "most different" up top
    df_run_info = df_run_info.sort_values(by="ABS((new-std)/std)", ascending=False)
    return df_run_info


def writeRunInfoFromDF(df_run_info, target_var, output_folder_analyses_path):
    var_name_slugified = slugify(target_var)
    var_sens_csv_file_name = "sens_{0}.csv".format(var_name_slugified)
    output_analysis_path = os.path.join(output_folder_analyses_path, var_sens_csv_file_name)
    df_run_info.to_csv(output_analysis_path, index=False)
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
