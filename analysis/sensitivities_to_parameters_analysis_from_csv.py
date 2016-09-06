#Std
import math #for sqrt
import numpy as np
import logging
logger = logging.getLogger("--Sensitivities mos writer--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux
def main():
    # kwargs = {
    #     "perturbed_csvs_path_and_info_pairs": [("tmp/modelica_outputs/2016-08-25/10_39_00/agr_inp_init_perturbated.csv","agr_inp_init_perturbed")],
    #     "std_run_csv_path": "resource/standard_run.csv",
    #     "target_var": "population",
    #     "percentage_perturbed":"10",
    #     "specific_year":1950,
    #     "output_analysis_path": "tmp/asd.txt",
    # }
    # analyzeSensitivitiesFromVariableToParametersFromCSVs(**kwargs)
    pass
def analyzeSensitivitiesFromVariableToParametersFromCSVs(perturbed_csvs_path_and_info_pairs,target_var,percentage_perturbed,specific_year,rms_first_year,rms_last_year,std_run_csv_path,output_analysis_path):
    # The column order is hardcoded for now.
    headers = "parameter,parameter_default,parameter_perturbed_{percentage}_percent,{var_name}_{specific_year}_std,{var_name}_{specific_year}_new,std/new,(new-std)/std,ABS((new-std)/std),root_mean_square_{rms_first_year}_to_{rms_last_year},perturbed_param_csv_path".format(percentage=percentage_perturbed,var_name=target_var,specific_year=specific_year,rms_first_year=rms_first_year,rms_last_year=rms_last_year)
    rows_strs = [headers]
    for csv_path,param_info in perturbed_csvs_path_and_info_pairs:
        param_name = param_info[0]
        param_default = param_info[1]
        param_new_value = param_info[2]
        var_std_value_for_year = varValueForYear(target_var,specific_year,std_run_csv_path)
        var_new_value_for_year = varValueForYear(target_var,specific_year,csv_path)
        std_div_new = var_std_value_for_year/var_new_value_for_year
        perturbation_proportion = (var_new_value_for_year-var_std_value_for_year)/var_std_value_for_year
        perturbation_proportion_abs = abs(perturbation_proportion)
        rootMeanSquare = rootMeanSquareForCsvAndYearsAndStateVarAndStdCSV(csv_path,rms_first_year,rms_last_year,target_var,std_run_csv_path)

        param_row_str = "{param_name},{param_default},{param_new_value},{var_std_value_for_year:.4f},{var_new_value_for_year:.4f},{std_div_new:.4f},{perturbation_proportion},{perturbation_proportion_abs},{rootMeanSquare},{perturbed_param_csv_path}".format(param_name=param_name,param_default=param_default,param_new_value=param_new_value,var_std_value_for_year = var_std_value_for_year, var_new_value_for_year = var_new_value_for_year, std_div_new = std_div_new,perturbation_proportion=perturbation_proportion,perturbation_proportion_abs=perturbation_proportion_abs,rootMeanSquare=rootMeanSquare,perturbed_param_csv_path=csv_path)
        rows_strs.append(param_row_str)
    final_str = "\n".join(rows_strs)
    filesystem.files_aux.writeStrToFile(final_str,output_analysis_path)
    logger.debug("Wrote analysis for sensitivities to param to path:{path}".format(path=output_analysis_path))


def rootMeanSquareForCsvAndYearsAndStateVarAndStdCSV(perturbed_csv_path,first_year,last_year,state_var,std_run_csv_path):
    # Following the formula:  sqrt(1/n * (x_1^2 + x_2^2 + ... + x_n^2) )
    years_list = range(first_year,last_year+1)
    n = len(years_list)
    accum_squares_sum = 0
    for year in years_list:
        std_run_var_value = varValueForYear(state_var,year,std_run_csv_path)
        perturbed_var_value = varValueForYear(state_var,year,perturbed_csv_path)
        x_i = std_run_var_value-perturbed_var_value
        accum_squares_sum = accum_squares_sum + x_i^2
    rms = math.sqrt(accum_squares_sum)
    return rms

def varValueForYear(target_var,specific_year,file_path):
    data = np.genfromtxt(file_path, delimiter=',', names=True)
    year_index = np.where(data["time"]==specific_year)[0][0]
    value = data[target_var][year_index]
    return value


if __name__ == "__main__":
    main()


