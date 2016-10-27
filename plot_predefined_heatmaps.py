#Standard
import os
#Mine
import filesystem.files_aux
import plotting.plot_heatmap
def main():
    base_path = filesystem.files_aux.makeOutputPath("heatmaps")
    # Generate Theo Sens heatmaps:
    omTheoParamSens_1901_all_Heatmap(base_path)
    omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    # Generate Empirical heatmaps
    omEmpiricalParamSens_newMinusStdDivStd_1901and2001_all_heatmap(base_path)
    omEmpiricalParamSens_newMinusStdDivStd_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    omEmpiricalParamSens_rootMeanSquares_1901and2001_all_heatmap(base_path)
    omEmpiricalParamSens_rootMeanSquares_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
############## Special Heatmaps ######################3
###### EMPIRICAL SENS HEATMAPS ############
## (new-std)std for 1901 and 2100
# All vars
def omEmpiricalParamSens_newMinusStdDivStd_1901and2001_all_heatmap(base_path):
    for year in ["1901","2100"]:
        input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/new_minus_std_div_std_perturbed_5percent_"+year+"yr.csv" 
        plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using (std-new)/new formula for the year "+year
        plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_newMinusStdDivStd_"+year+"_all_heatmap")
        os.makedirs(plot_folder_path)
        plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)
# Workpackage1 params and vars for 1901 and 2100 sens
def omEmpiricalParamSens_newMinusStdDivStd_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    for year in ["1901","2100"]:
        input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/new_minus_std_div_std_perturbed_5percent_"+year+"yr.csv"
        plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using (std-new)/new formula for the year "+year+".\nOnly the variables and parameters studied in WorkPackage 1"
        plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_newMinusStdDivStd_onlyWorkPackage1ParamsAndVars"+year+"_all_heatmap")
        os.makedirs(plot_folder_path)
        plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)
## Root mean squares for 1901 and 2100
# All vars
def omEmpiricalParamSens_rootMeanSquares_1901and2001_all_heatmap(base_path):
    for year in ["1901","2100"]:
        input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/root_mean_squares_perturbed_5percent_From1900To"+year+".csv"
        plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using root mean squares for all the years between 1900 and "+year
        plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_rootMeanSquares"+year+"_all_heatmap")
        os.makedirs(plot_folder_path)
        plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)
# Workpackage1 params and vars for 1901 and 2100 sens
def omEmpiricalParamSens_rootMeanSquares_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    for year in ["1901","2100"]:
        input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/root_mean_squares_perturbed_5percent_From1900To"+year+".csv"
        plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using root mean squares for all the years between 1900 and "+year+".\nOnly the variables and parameters studied in WorkPackage 1"
        plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_rootMeanSquares_onlyWorkPackage1ParamsAndVars"+year+"_all_heatmap")
        os.makedirs(plot_folder_path)
        plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)

###### THEO SENS HEATMAPS ############
# All params and vars for 1901 sens
def omTheoParamSens_1901_all_Heatmap(base_path):
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nAll variables and parameters from Sensitivity Analysis, including new differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_all_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)

# Workpackage1 params and vars for 1901 sens
def omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nOnly the variables and parameters studied in WorkPackage 1"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
