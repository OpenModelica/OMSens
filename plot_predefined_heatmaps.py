#Standard
import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--Heatmap Plotting script--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux
import plotting.plot_heatmap
def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # to show logging info into STDOUT
    base_path = filesystem.files_aux.makeOutputPath("heatmaps")
    # Generate Theo Sens heatmaps:
    ## Vanilla
    # omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_VanillaW3_all_heatmap(base_path)
    ## Population state var new
    omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveInfluenceIn1901_heatmap(base_path)
    omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_all_Heatmap(base_path)
    # omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    # # Generate Empirical heatmaps
    # ## (new - std) /std
    # omEmpiricalParamSens_newMinusStdDivStd_1901and2001_all_heatmap(base_path)
    # omEmpiricalParamSens_newMinusStdDivStd_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    # ## RMS
    # omEmpiricalParamSens_rootMeanSquares_1901and2001_all_heatmap(base_path)
    # omEmpiricalParamSens_rootMeanSquares_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)

############## Predefined Heatmaps ######################3
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
## Vanilla
# Heatmap of vanilla matrix for 1901 only including influencer params
def omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveInfluenceIn1901_heatmap(base_path):
    influencers_params =[ "p_fr_cap_al_obt_res_2[4]", "ind_mtl_emiss_fact", "p_avg_life_ind_cap_1", "ind_mtl_toxic_index", "p_fr_cap_al_obt_res_2[3]", "p_avg_life_agr_inp_2", "agr_mtl_toxic_index", "assim_half_life_1970", "life_expect_norm", "arable_land_init", "ppoll_trans_del", "lifet_perc_del", "processing_loss", "p_yield_tech_chg_mlt[4]", "perc_food_ratio_init", "agr_inp_init"]
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_vanilla.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Vanilla World3-Modelica\nAll variables but only parameters that have influence from IDAsens, NOT including extra differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=influencers_params)
# Heatmap of vanilla matrix for 1901 only including non-influencer params
def omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path):
    nonInfluencers_params = ['p_fr_cap_al_obt_res_2[10]','p_ppoll_tech_chg_mlt[3]','ind_out_pc_des','p_ppoll_tech_chg_mlt[2]','labor_util_fr_del_time','service_capital_init','labor_force_partic','p_res_tech_chg_mlt[2]','social_discount','inherent_land_fert','pop1_init','p_avg_life_serv_cap_2','food_short_perc_del','t_zero_pop_grow_time','t_policy_year','pot_arable_land_tot','t_ind_equil_time','des_compl_fam_size_norm','des_food_ratio_dfr','p_fr_cap_al_obt_res_2[6]','ind_out_in_1970','p_serv_cap_out_ratio_1','pers_pollution_init','p_fr_cap_al_obt_res_2[5]','res_tech_init','des_ppoll_index_DPOLX','p_fr_cap_al_obt_res_2[11]','t_pop_equil_time','p_fr_cap_al_obt_res_2[9]','pot_arable_land_init','reproductive_lifetime','p_ppoll_gen_fact_1','tech_dev_del_TDD','t_land_life_time','yield_tech_init','t_fert_cont_eff_time','p_ppoll_tech_chg_mlt[4]','p_fr_cap_al_obt_res_2[2]','labor_util_fr_del_init','p_ind_cap_out_ratio_1','fr_agr_inp_pers_mtl','frac_res_pers_mtl','social_adj_del','des_res_use_rt_DNRUR','income_expect_avg_time','p_fr_cap_al_obt_res_2[1]','p_res_tech_chg_mlt[1]','subsist_food_pc','p_yield_tech_chg_mlt[1]','industrial_capital_init','p_ppoll_tech_chg_mlt[1]','land_fertility_init','pop2_init','t_fcaor_time','ppoll_tech_init','urban_ind_land_init','ppoll_in_1970','p_fr_cap_al_obt_res_2[8]','p_land_yield_fact_1','hlth_serv_impact_del','urb_ind_land_dev_time','land_fr_harvested','p_yield_tech_chg_mlt[2]','pop3_init','p_res_tech_chg_mlt[3]','p_fioa_cons_const_2','pop4_init','p_serv_cap_out_ratio_2','avg_life_land_norm','p_nr_res_use_fact_1','max_tot_fert_norm','p_fr_cap_al_obt_res_2[7]','p_avg_life_serv_cap_1','t_air_poll_time','nr_resources_init','p_res_tech_chg_mlt[4]','p_avg_life_agr_inp_1','p_avg_life_ind_cap_2','p_yield_tech_chg_mlt[3]','p_fioa_cons_const_1']
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_vanilla.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Vanilla World3-Modelica\nAll variables but only parameters that have NO influence from IDAsens, NOT including extra differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveNoInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=nonInfluencers_params)
# Heatmap of all vars but using vanilla w3 instead of the version that includes a new state population variable
def omTheoParamSens_1901_VanillaW3_all_heatmap(base_path):
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_vanilla.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Vanilla World3-Modelica\nAll variables and parameters from IDAsens, NOT including extra differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_VanillaW3_all_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)
## Population function modified
# Heatmap of population function modified matrix for 1901 only including influencer params
def omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveInfluenceIn1901_heatmap(base_path):
    influencers_params =[ "p_fr_cap_al_obt_res_2[4]", "ind_mtl_emiss_fact", "p_avg_life_ind_cap_1", "ind_mtl_toxic_index", "p_fr_cap_al_obt_res_2[3]", "p_avg_life_agr_inp_2", "agr_mtl_toxic_index", "assim_half_life_1970", "life_expect_norm", "arable_land_init", "ppoll_trans_del", "lifet_perc_del", "processing_loss", "p_yield_tech_chg_mlt[4]", "perc_food_ratio_init", "agr_inp_init"]
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Population New State Var World3-Modelica\nAll variables but only parameters that have influence from IDAsens, NOT including extra differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=influencers_params)
# Heatmap of vanilla matrix for 1901 only including non-influencer params
def omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path):
    nonInfluencers_params = ['p_fr_cap_al_obt_res_2[10]','p_ppoll_tech_chg_mlt[3]','ind_out_pc_des','p_ppoll_tech_chg_mlt[2]','labor_util_fr_del_time','service_capital_init','labor_force_partic','p_res_tech_chg_mlt[2]','social_discount','inherent_land_fert','pop1_init','p_avg_life_serv_cap_2','food_short_perc_del','t_zero_pop_grow_time','t_policy_year','pot_arable_land_tot','t_ind_equil_time','des_compl_fam_size_norm','des_food_ratio_dfr','p_fr_cap_al_obt_res_2[6]','ind_out_in_1970','p_serv_cap_out_ratio_1','pers_pollution_init','p_fr_cap_al_obt_res_2[5]','res_tech_init','des_ppoll_index_DPOLX','p_fr_cap_al_obt_res_2[11]','t_pop_equil_time','p_fr_cap_al_obt_res_2[9]','pot_arable_land_init','reproductive_lifetime','p_ppoll_gen_fact_1','tech_dev_del_TDD','t_land_life_time','yield_tech_init','t_fert_cont_eff_time','p_ppoll_tech_chg_mlt[4]','p_fr_cap_al_obt_res_2[2]','labor_util_fr_del_init','p_ind_cap_out_ratio_1','fr_agr_inp_pers_mtl','frac_res_pers_mtl','social_adj_del','des_res_use_rt_DNRUR','income_expect_avg_time','p_fr_cap_al_obt_res_2[1]','p_res_tech_chg_mlt[1]','subsist_food_pc','p_yield_tech_chg_mlt[1]','industrial_capital_init','p_ppoll_tech_chg_mlt[1]','land_fertility_init','pop2_init','t_fcaor_time','ppoll_tech_init','urban_ind_land_init','ppoll_in_1970','p_fr_cap_al_obt_res_2[8]','p_land_yield_fact_1','hlth_serv_impact_del','urb_ind_land_dev_time','land_fr_harvested','p_yield_tech_chg_mlt[2]','pop3_init','p_res_tech_chg_mlt[3]','p_fioa_cons_const_2','pop4_init','p_serv_cap_out_ratio_2','avg_life_land_norm','p_nr_res_use_fact_1','max_tot_fert_norm','p_fr_cap_al_obt_res_2[7]','p_avg_life_serv_cap_1','t_air_poll_time','nr_resources_init','p_res_tech_chg_mlt[4]','p_avg_life_agr_inp_1','p_avg_life_ind_cap_2','p_yield_tech_chg_mlt[3]','p_fioa_cons_const_1']
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Population New State Var World3-Modelica\nAll variables but only parameters that have NO influence from IDAsens, NOT including extra differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveNoInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=nonInfluencers_params)
# All params and vars for 1901 sens
def omTheoParamSens_1901_all_Heatmap(base_path):
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Population New State Var World3-Modelica\nAll variables and parameters from Sensitivity Analysis, including new differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_all_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)

# Workpackage1 params and vars for 1901 sens
def omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Population New State Var World3-Modelica\nOnly the variables and parameters studied in WorkPackage 1"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
