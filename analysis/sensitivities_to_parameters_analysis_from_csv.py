#Std
import sys #for logging stdout
import math #for sqrt
import numpy as np
import logging
logger = logging.getLogger("--Sensitivities To parameters analysis--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux
def main():
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # kwargs = {
    #     "perturbed_csvs_path_and_info_pairs": [("resource/standard_run.csv","std_run_2")],
    #     "std_run_csv_path": "resource/standard_run.csv",
    #     "target_var": "population",
    #     "percentage_perturbed":"10",
    #     "specific_year":1950,
    #     "output_analysis_path": "tmp/asd_2.txt",
    #     "rms_first_year": 1900,
    #     "rms_last_year": 2100,
    # }
    # analyzeSensitivitiesFromVariableToParametersFromCSVs(**kwargs)
    pass
def analyzeSensitivitiesFromVariableToParametersFromCSVs(perturbed_csvs_path_and_info_pairs,target_var,percentage_perturbed,specific_year,rms_first_year,rms_last_year,std_run_csv_path,output_analysis_path):
    # The column order is hardcoded for now.
    headers = "parameter,parameter_default,parameter_perturbed_{percentage}_percent,{var_name}_{specific_year}_std,{var_name}_{specific_year}_new,std/new,(new-std)/std,ABS((new-std)/std),root_mean_square_{rms_first_year}_to_{rms_last_year},perturbed_param_csv_path".format(percentage=percentage_perturbed,var_name=target_var,specific_year=specific_year,rms_first_year=rms_first_year,rms_last_year=rms_last_year)
    rows_strs = [headers]
    data_std_run = np.genfromtxt(std_run_csv_path, delimiter=',', names=True)
    for csv_path,param_info in perturbed_csvs_path_and_info_pairs:
        param_name = param_info[0]
        param_default = param_info[1]
        param_new_value = param_info[2]
        data_perturbed_parameter = np.genfromtxt(csv_path, delimiter=',', names=True)
        var_std_value_for_year = varValueForYear(target_var,specific_year,data_std_run)
        var_new_value_for_year = varValueForYear(target_var,specific_year,data_perturbed_parameter)
        std_div_new = var_std_value_for_year/var_new_value_for_year
        perturbation_proportion = (var_new_value_for_year-var_std_value_for_year)/var_std_value_for_year
        perturbation_proportion_abs = abs(perturbation_proportion)
        rootMeanSquare = rootMeanSquareForCsvAndYearsAndStateVarAndStdCSV(data_perturbed_parameter,rms_first_year,rms_last_year,target_var,data_std_run)

        param_row_str = "{param_name},{param_default},{param_new_value},{var_std_value_for_year:.4f},{var_new_value_for_year:.4f},{std_div_new:.4f},{perturbation_proportion},{perturbation_proportion_abs},{rootMeanSquare},{perturbed_param_csv_path}".format(param_name=param_name,param_default=param_default,param_new_value=param_new_value,var_std_value_for_year = var_std_value_for_year, var_new_value_for_year = var_new_value_for_year, std_div_new = std_div_new,perturbation_proportion=perturbation_proportion,perturbation_proportion_abs=perturbation_proportion_abs,rootMeanSquare=rootMeanSquare,perturbed_param_csv_path=csv_path)
        rows_strs.append(param_row_str)
    final_str = "\n".join(rows_strs)
    filesystem.files_aux.writeStrToFile(final_str,output_analysis_path)
    logger.debug("Wrote analysis for sensitivities to param to path:{path}".format(path=output_analysis_path))


def rootMeanSquareForCsvAndYearsAndStateVarAndStdCSV(data_perturbed_parameter,first_year,last_year,state_var,data_std_run):
    # Following the formula:  sqrt(1/n * (x_1^2 + x_2^2 + ... + x_n^2) )
    years_list = range(first_year,last_year+1) #get a list for
    n = last_year - first_year + 1  # how many years to include
    logger.debug("Writing Root Mean Squares")
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


if __name__ == "__main__":
    main()


