#Standard
import os
#Mine
import filesystem.files_aux
import plotting.plot_heatmap
def main():
    base_path = filesystem.files_aux.makeOutputPath("heatmaps")
    # omTheoParamSens_1901_all_Heatmap(base_path)
    # omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    asd(base_path)
### Special Heatmaps
### BORRAME O ADAPTAME:
def asd(base_path):
    input_matrix_path = "resource/paramVarSensMatrix/1901/new_minus_std_div_std_perturbed_5_percent_1901yr.csv"
    # input_matrix_path = "resource/w3_only1901_time_fix_paramvarmatrix.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nAll variables and parameters from Sensitivity Analysis"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_all_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)
### BORRAME O ADAPTAME^

# All params and vars for 1901 sens
def omTheoParamSens_1901_all_Heatmap(base_path):
    input_matrix_path = "resource/w3_only1901_time_fix_paramvarmatrix.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nAll variables and parameters from Sensitivity Analysis"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_all_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)

# Workpackage1 params and vars for 1901 sens
def omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    input_matrix_path = "resource/w3_only1901_time_fix_paramvarmatrix.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for World3-Modelica\nOnly the variables and parameters studied in WorkPackage 1"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
