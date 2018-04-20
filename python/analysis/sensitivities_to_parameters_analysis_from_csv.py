#Std
import sys #for logging stdout
import os  # for os.path
import math #for sqrt
import pandas # dataframes
import unicodedata  # slugifying file names
import re # regular expressions
import numpy as np
import logging
logger = logging.getLogger("--Sensitivities To parameters analysis--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux

def analyzeSensitivitiesFromManyVariablesToParametersAndCreateParamVarMatrices(perturbed_csvs_path_and_info_pairs,target_vars,percentage_perturbed,specific_year,rms_first_year,rms_last_year,std_run_csv_path,output_folder_analyses_path):
    # Initialize dict with rows for each variable. Each row will correspond to the values of said variable for a respective run from each respective parameter perturbed
    vars_rows_dicts = {var_name:[] for var_name in target_vars}
    # Read standard run output that we will use as default output
    df_std_run = pandas.read_csv(std_run_csv_path,index_col=0)
    for param_csv_path,param_info in perturbed_csvs_path_and_info_pairs:
        # Read perturbed parameter csv
        df_param_perturbed = pandas.read_csv(param_csv_path,index_col=0)
        # Get param info such as name, default value, etc
        param_name = param_info[0]
        param_default = param_info[1]
        param_new_value = param_info[2]
        # Iterate variables getting the values in the perturbed param csv
        for target_var in target_vars:
            # Get values for variable from standard run and perturbed run outputs and an specific year
            var_std_value_for_year = df_std_run[target_var][specific_year]
            var_new_value_for_year = df_param_perturbed[target_var][specific_year]
            # Calculate sensitivity methods for an specific year
            std_div_new = var_std_value_for_year/var_new_value_for_year
            perturbation_proportion = (var_new_value_for_year-var_std_value_for_year)/var_std_value_for_year
            perturbation_proportion_abs = abs(perturbation_proportion)
            # Calculate sensitivity methods for the whole run
            rootMeanSquare = rootMeanSquareForVar(df_std_run,df_param_perturbed,rms_first_year,rms_last_year,target_var)
            param_row_dict = {
                "parameter"                                                        : param_name,
                "parameter_default"                                                : param_default,
                "parameter_perturbed_{0}_percent".format(percentage_perturbed)     : param_new_value,
                "std_at_t_{0}".format(specific_year)                               : var_std_value_for_year,
                "new_at_t_{0}".format(specific_year)                               : var_new_value_for_year,
                "std/new"                                                          : std_div_new,
                "(new-std)/std"                                                    : perturbation_proportion,
                "ABS((new-std)/std)"                                               : perturbation_proportion_abs,
                "root_mean_square_{0}_to_{1}".format(rms_first_year,rms_last_year) : rootMeanSquare,
                "perturbed_param_csv_path"                                         : param_csv_path,
            }
            # Add this row to the rows of this respective variable
            var_rows = vars_rows_dicts[target_var]
            var_rows.append(param_row_dict)
    # Set the columns order of the sensitivity analysis csv
    columns_order = [
        "parameter",
        "parameter_default",
        "parameter_perturbed_{0}_percent".format(percentage_perturbed),
        "std_at_t_{0}".format(specific_year),
        "new_at_t_{0}".format(specific_year),
        "std/new",
        "(new-std)/std",
        "ABS((new-std)/std)",
        "root_mean_square_{0}_to_{1}".format(rms_first_year,rms_last_year),
        "perturbed_param_csv_path",
    ]
    # Create a df for each var using its rows
    for target_var in target_vars:
        var_rows = vars_rows_dicts[target_var]
        df_sens = pandas.DataFrame.from_records(var_rows, columns=columns_order)
        # Sort by diff column so we get the "most different" up top
        df_sens = df_sens.sort_values(by="ABS((new-std)/std)", ascending=False)
        # Write sensitivity df to csv file
        var_name_slugified     = slugify(target_var)
        var_sens_csv_file_name = "sens_{0}.csv".format(var_name_slugified)
        output_analysis_path   = os.path.join(output_folder_analyses_path,var_sens_csv_file_name)
        df_sens.to_csv(output_analysis_path,index=False)

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value)
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value


def rootMeanSquareForVar(df_std_run,df_param_perturbed,rms_first_year,rms_last_year,target_var):
    # Get the columns from year to year indicated for std run and perturbed param run
    col_subyrs_std       =         df_std_run[target_var].loc[rms_first_year:rms_last_year]
    col_subyrs_perturbed = df_param_perturbed[target_var].loc[rms_first_year:rms_last_year]
    # Assert that both columns have the same number of rows
    # Calculate root mean square from both columns
    diff = col_subyrs_std - col_subyrs_perturbed
    diff_squared = diff**2
    mean_diff_squared = sum(diff_squared)/len(diff_squared)
    rms = math.sqrt(mean_diff_squared)
    return rms

# Old version:
    # CAREFUL! The order is hardcoded for now
    # The first column of the first row is "param_perturbed_5_percent" and the following columns correspond to the variable names
    first_row_only_rms = ",".join(["param_perturbed_{percentage_perturbed}_percent".format(percentage_perturbed=percentage_perturbed)]+target_vars_list)
    first_row_others = ",".join(["param_perturbed_{percentage_perturbed}_percent_{specific_year}yr".format(percentage_perturbed=percentage_perturbed,specific_year=specific_year)]+target_vars_list)
    std_div_new_matrix_rows_str = first_row_others
    new_minus_std_div_std_matrix_rows_str = first_row_others
    root_mean_square_matrix_rows_str = first_row_only_rms

    headers = "std/new,(new-std)/std,ABS((new-std)/std),root_mean_square_{rms_first_year}_to_{rms_last_year},perturbed_param_csv_path"

    data_std_run = np.genfromtxt(std_run_csv_path, delimiter=',', names=True,deletechars="""~!@#$%^&*()=+~\|]}[{';: /?>,<""")  # deletechars="..." so it doesn't remove dots
    # import ipdb;ipdb.set_trace()
    i= 0 # to count analysed params for now
    for csv_path,param_info in perturbed_csvs_path_and_info_pairs:
        # Retrieve param info from tuple
        param_name = param_info[0]
        param_default = param_info[1]
        param_new_value = param_info[2]
        data_perturbed_parameter = np.genfromtxt(csv_path, delimiter=',', names=True,deletechars="""~!@#$%^&*()=+~\|]}[{';: /?>,<""")  # deletechars="..." so it doesn't remove dots
        # Set param_name as first cell of this row
        std_div_new_matrix_row = param_name
        new_minus_std_div_std_matrix_row = param_name
        root_mean_square_matrix_row = param_name
        ### Log each time 10 params have been analyzed
        if (i % 10 == 0):
            logger.debug("Have analyzed: {i} params of {len_list}. Next param: {param_name}".format(i=i,len_list=len(perturbed_csvs_path_and_info_pairs),param_name=param_name))
        for var_influenced in target_vars_list:
            var_std_value_for_year = varValueForYear(var_influenced,specific_year,data_std_run)
            var_new_value_for_year = varValueForYear(var_influenced,specific_year,data_perturbed_parameter)
            std_div_new = var_std_value_for_year/var_new_value_for_year
            perturbation_proportion = (var_new_value_for_year-var_std_value_for_year)/var_std_value_for_year
            perturbation_proportion_abs = abs(perturbation_proportion)
            rootMeanSquare = rootMeanSquareForCsvAndYearsAndStateVarAndStdCSV(data_perturbed_parameter,rms_first_year,rms_last_year,var_influenced,data_std_run)
            #Finished a var for this row
            std_div_new_matrix_row = std_div_new_matrix_row +","+ str(std_div_new)
            new_minus_std_div_std_matrix_row = new_minus_std_div_std_matrix_row +","+ str(perturbation_proportion)
            root_mean_square_matrix_row = root_mean_square_matrix_row +","+ str(rootMeanSquare)
        # Finished all the vars for a row
        std_div_new_matrix_rows_str = std_div_new_matrix_rows_str + "\n" + std_div_new_matrix_row
        new_minus_std_div_std_matrix_rows_str = new_minus_std_div_std_matrix_rows_str + "\n" + new_minus_std_div_std_matrix_row
        root_mean_square_matrix_rows_str = root_mean_square_matrix_rows_str + "\n" + root_mean_square_matrix_row
        i=i+1  # to count analyzed params for now

    #Write matrices to file
    # For Root Mean Squares
    file_name = "root_mean_squares"+"_perturbed_{percentage_perturbed}percent_From{rms_first_year}To{rms_last_year}.csv".format(percentage_perturbed=percentage_perturbed,rms_first_year=rms_first_year,rms_last_year=rms_last_year)
    output_analysis_path = os.path.join(output_folder_analyses_path,file_name)
    filesystem.files_aux.writeStrToFile(root_mean_square_matrix_rows_str,output_analysis_path)
    logger.debug("Wrote analysis for sensitivities to param to path:{path}".format(path=output_analysis_path))

    #The matrices std_div_new and new_minus_std_div_std matrices are for a given year, so they will have that year in the file name
    matrix_name_and_fullStr_pairs = [("std_div_new",std_div_new_matrix_rows_str),("new_minus_std_div_std",new_minus_std_div_std_matrix_rows_str)]
    for matrix_name,fullStr in matrix_name_and_fullStr_pairs:
        file_name = matrix_name+"_perturbed_{percentage_perturbed}percent_{specific_year}yr.csv".format(percentage_perturbed=percentage_perturbed,specific_year=specific_year)
        output_analysis_path = os.path.join(output_folder_analyses_path,file_name)
        filesystem.files_aux.writeStrToFile(fullStr,output_analysis_path)
        logger.debug("Wrote analysis for sensitivities to param to path:{path}".format(path=output_analysis_path))
# Old version^


def rootMeanSquareForCsvAndYearsAndStateVarAndStdCSV(data_perturbed_parameter,first_year,last_year,state_var,data_std_run):
    # Following the formula:  sqrt(1/n * (x_1^2 + x_2^2 + ... + x_n^2) )
    years_list = range(first_year,last_year+1) #get a list for
    n = last_year - first_year + 1  # how many years to include
    # logger.debug("Writing Root Mean Squares")
    # We don't know if both datas have same years range. We have to get the correct range for this RMS calculation for both
    std_run_first_year_index = yearIndexForNdarray(data_std_run,first_year)# get year index for first year in rms for std run
    std_run_last_year_index = yearIndexForNdarray(data_std_run,last_year) #get year index for last year in rms for std run
    std_run_target_var_values_list = data_std_run[state_var][std_run_first_year_index:std_run_last_year_index] # get the list of values for the state_var corresponding the that the years range for this RMS

    perturbed_parameter_first_year_index = yearIndexForNdarray(data_perturbed_parameter,first_year)  # get year index for first year in rms for perturbed run
    perturbed_parameter_last_year_index = yearIndexForNdarray(data_perturbed_parameter,last_year)   # get year index for last year in rms for perturbed run
    perturbed_parameter_target_var_values_list = data_perturbed_parameter[state_var][perturbed_parameter_first_year_index:perturbed_parameter_last_year_index] # get the list of values for the state_var corresponding the that the years range for this RMS

    rms = math.sqrt(1/n*sum((std_run_target_var_values_list - perturbed_parameter_target_var_values_list)**2))

    return rms

def varValueForYear(target_var,specific_year,numpy_data):
    year_index = yearIndexForNdarray(numpy_data,specific_year)
    value = numpy_data[target_var][year_index]
    return value

def yearIndexForNdarray(numpy_data,year,year_col_name="time"):
    year_index = np.where(numpy_data[year_col_name]==year)[0][0]
    return year_index
