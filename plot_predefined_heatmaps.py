#Standard
import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--Heatmap Plotting script--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux
import plotting.plot_heatmap


def main():
    # to show logging info into STDOUT
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    base_path = filesystem.files_aux.makeOutputPath("heatmaps")
    # Generate Theo Sens heatmaps:
    ## Vanilla
    # omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_VanillaW3_all_heatmap(base_path)
    ## Population state var new
    # omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path)
    # omTheoParamSens_1901_PopStateVarNew_all_Heatmap(base_path)
    # omTheoParamSens_1901_PopStateVarNew_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    # Generate Empirical heatmaps
    ## (new - std) /std
    # omEmpiricalParamSens_newMinusStdDivStd_1901and2001_influencers_heatmap(base_path)
    # omEmpiricalParamSens_newMinusStdDivStd_1901and2001_all_heatmap(base_path)
    omEmpiricalParamSens_newMinusStdDivStd_2100_all_paper_heatmap(base_path)
    # omEmpiricalParamSens_newMinusStdDivStd_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)
    ## RMS
    # omEmpiricalParamSens_rootMeanSquares_1901and2001_influencers_heatmap(base_path)
    # omEmpiricalParamSens_rootMeanSquares_1901and2001_all_heatmap(base_path)
    # omEmpiricalParamSens_rootMeanSquares_1901and2100_onlyWorkPackage1ParamsAndVars_Heatmap(base_path)

############## Predefined Heatmaps ######################3
###### EMPIRICAL SENS HEATMAPS ############
## (new-std)std for 1901 and 2100
# Only noninfluencers for 1901 and 2100
def omEmpiricalParamSens_newMinusStdDivStd_1901and2001_influencers_heatmap(base_path):
    # Only one parameter difference between influencers1901 and influencers2100
    influencer_2100_butNot1901_newMinusStdDivStd = ['des_compl_fam_size_norm']
    # First initialize the self contained lists and then add the conflicting parameter to the corresponding lists
    influencers_1901_newMinusStdDivStd           = ["tech_dev_del_TDD", "industrial_capital_init", "p_ind_cap_out_ratio_1", "ppoll_trans_del", "social_adj_del", "lifet_perc_del", "pop2_init", "arable_land_init", "land_fertility_init", "pop1_init", "res_tech_init", "yield_tech_init", "ppoll_tech_init", "life_expect_norm", "land_fr_harvested", "p_land_yield_fact_1", "p_ppoll_gen_fact_1", "pot_arable_land_init", "agr_inp_init", "pop3_init", "service_capital_init", "nr_resources_init", "subsist_food_pc", "frac_res_pers_mtl", "ind_mtl_toxic_index", "ind_mtl_emiss_fact", "agr_mtl_toxic_index", "fr_agr_inp_pers_mtl", "pot_arable_land_tot", "p_serv_cap_out_ratio_1", "pop4_init", "pers_pollution_init", "hlth_serv_impact_del", "urban_ind_land_init", "labor_util_fr_del_init", "perc_food_ratio_init", "labor_force_partic", "p_fioa_cons_const_1", "assim_half_life_1970", "processing_loss", "max_tot_fert_norm", "inherent_land_fert", "reproductive_lifetime", "p_avg_life_ind_cap_1", "social_discount", "p_avg_life_serv_cap_1", "p_avg_life_agr_inp_1", "labor_util_fr_del_time", "food_short_perc_del", "urb_ind_land_dev_time", "income_expect_avg_time", "ppoll_in_1970", "avg_life_land_norm", "p_nr_res_use_fact_1",]
    noninfluencers_2100_newMinusStdDivStd        = ["p_ppoll_tech_chg_mlt[3]", "t_fcaor_time", "p_fr_cap_al_obt_res_2[10]", "p_fr_cap_al_obt_res_2[9]", "p_fr_cap_al_obt_res_2[8]", "des_res_use_rt_DNRUR", "des_ppoll_index_DPOLX", "p_fr_cap_al_obt_res_2[7]", "des_food_ratio_dfr", "t_air_poll_time", "t_fert_cont_eff_time", "p_ppoll_tech_chg_mlt[4]", "t_ind_equil_time", "t_land_life_time", "t_policy_year", "t_pop_equil_time", "t_zero_pop_grow_time", "p_fr_cap_al_obt_res_2[6]", "p_fr_cap_al_obt_res_2[5]", "p_fr_cap_al_obt_res_2[11]", "ind_out_in_1970", "ind_out_pc_des", "p_fr_cap_al_obt_res_2[2]", "p_res_tech_chg_mlt[1]", "p_res_tech_chg_mlt[2]", "p_res_tech_chg_mlt[3]", "p_res_tech_chg_mlt[4]", "p_avg_life_ind_cap_2", "p_serv_cap_out_ratio_2", "p_yield_tech_chg_mlt[1]", "p_yield_tech_chg_mlt[2]", "p_yield_tech_chg_mlt[3]", "p_yield_tech_chg_mlt[4]", "p_ppoll_tech_chg_mlt[2]", "p_fr_cap_al_obt_res_2[4]", "p_avg_life_agr_inp_2", "p_ppoll_tech_chg_mlt[1]", "p_avg_life_serv_cap_2", "p_fioa_cons_const_2", "p_fr_cap_al_obt_res_2[1]", "p_fr_cap_al_obt_res_2[3]",]
    noninfluencers_1901_newMinusStdDivStd = noninfluencers_2100_newMinusStdDivStd + influencer_2100_butNot1901_newMinusStdDivStd
    influencers_2100_newMinusStdDivStd = influencers_1901_newMinusStdDivStd + influencer_2100_butNot1901_newMinusStdDivStd
    # Put them into dict so I don't have to breakdown the "for loop"
    influencers_and_noninfluencers_dict = {
        "1901": {"noninfluencers":noninfluencers_1901_newMinusStdDivStd,
               "influencers": influencers_1901_newMinusStdDivStd,
               },
        "2100": {"noninfluencers":noninfluencers_2100_newMinusStdDivStd,
               "influencers": influencers_2100_newMinusStdDivStd,
               }
    }
    for year in ["1901","2100"]:
        influencers = influencers_and_noninfluencers_dict[year]["influencers"]
        noninfluencers = influencers_and_noninfluencers_dict[year]["noninfluencers"]
        input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/new_minus_std_div_std_perturbed_5percent_"+year+"yr.csv"
        # Plot influencers
        plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using (std-new)/new formula for the year "+year+". Only parameters that have effect."
        plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_newMinusStdDivStd_"+year+"_onlyInfluencers_heatmap")
        os.makedirs(plot_folder_path)
        plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=influencers)
        # Plot noninfluencers
        # plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using (std-new)/new formula for the year "+year+". Only parameters that have NO effect."
        # plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_newMinusStdDivStd_"+year+"_onlyNonnfluencers_heatmap")
        # os.makedirs(plot_folder_path)
        # plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=noninfluencers)
# All vars
def omEmpiricalParamSens_newMinusStdDivStd_2100_all_paper_heatmap(base_path):
    year = "2100"
    input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/new_minus_std_div_std_perturbed_5percent_"+year+"yr.csv"
    plot_title = ""
    plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_newMinusStdDivStd_"+year+"_all_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)
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
# Only noninfluencers for 1901 and 2100
def omEmpiricalParamSens_rootMeanSquares_1901and2001_influencers_heatmap(base_path):
    # Parameters differences between influencers in 1901 and 2100 ( all of the ones in 1901 included in 2100)
    # influencers_2100_butNot1901_rms = ['p_fioa_cons_const_1', 'p_ind_cap_out_ratio_1', 'p_avg_life_ind_cap_1', 'life_expect_norm', 'reproductive_lifetime', 'p_serv_cap_out_ratio_1', 'land_fr_harvested', 'inherent_land_fert', 'p_land_yield_fact_1', 'des_compl_fam_size_norm', 'subsist_food_pc', 'max_tot_fert_norm', 'p_nr_res_use_fact_1', 'p_avg_life_serv_cap_1', 'pot_arable_land_tot', 'processing_loss', 'lifet_perc_del', 'income_expect_avg_time', 'p_ppoll_gen_fact_1', 'avg_life_land_norm', 'assim_half_life_1970', 'ppoll_in_1970', 'p_avg_life_agr_inp_1', 'social_discount', 'social_adj_del', 'ind_mtl_toxic_index', 'ind_mtl_emiss_fact', 'frac_res_pers_mtl', 'agr_mtl_toxic_index', 'fr_agr_inp_pers_mtl', 'ppoll_trans_del', 'hlth_serv_impact_del', 'labor_force_partic', 'urb_ind_land_dev_time', 'food_short_perc_del', 'labor_util_fr_del_time', 'tech_dev_del_TDD']
    # 1901
    noninfluencers_1901_rms = ["ind_out_pc_des", "hlth_serv_impact_del", "ppoll_in_1970", "pot_arable_land_tot", "des_ppoll_index_DPOLX", "des_res_use_rt_DNRUR", "food_short_perc_del", "fr_agr_inp_pers_mtl", "frac_res_pers_mtl", "income_expect_avg_time", "ppoll_trans_del", "p_yield_tech_chg_mlt[4]", "p_yield_tech_chg_mlt[3]", "p_yield_tech_chg_mlt[2]", "p_yield_tech_chg_mlt[1]", "p_serv_cap_out_ratio_2", "p_serv_cap_out_ratio_1", "p_res_tech_chg_mlt[4]", "des_food_ratio_dfr", "processing_loss", "inherent_land_fert", "t_ind_equil_time", "assim_half_life_1970", "urb_ind_land_dev_time", "tech_dev_del_TDD", "t_zero_pop_grow_time", "t_pop_equil_time", "t_policy_year", "t_land_life_time", "t_fert_cont_eff_time", "reproductive_lifetime", "t_fcaor_time", "t_air_poll_time", "subsist_food_pc", "social_discount", "social_adj_del", "avg_life_land_norm", "des_compl_fam_size_norm", "p_res_tech_chg_mlt[3]", "p_res_tech_chg_mlt[2]", "p_res_tech_chg_mlt[1]", "ind_mtl_emiss_fact", "p_fioa_cons_const_1", "p_avg_life_serv_cap_2", "p_avg_life_serv_cap_1", "p_avg_life_ind_cap_2", "p_avg_life_ind_cap_1", "p_avg_life_agr_inp_2", "p_avg_life_agr_inp_1", "max_tot_fert_norm", "p_ppoll_tech_chg_mlt[4]", "lifet_perc_del", "life_expect_norm", "land_fr_harvested", "ind_mtl_toxic_index", "labor_util_fr_del_time", "ind_out_in_1970", "labor_force_partic", "p_fioa_cons_const_2", "p_fr_cap_al_obt_res_2[1]", "p_fr_cap_al_obt_res_2[2]", "p_fr_cap_al_obt_res_2[3]", "p_ppoll_tech_chg_mlt[3]", "p_ppoll_tech_chg_mlt[2]", "p_ppoll_tech_chg_mlt[1]", "p_ppoll_gen_fact_1", "p_nr_res_use_fact_1", "p_land_yield_fact_1", "agr_mtl_toxic_index", "p_fr_cap_al_obt_res_2[11]", "p_fr_cap_al_obt_res_2[10]", "p_fr_cap_al_obt_res_2[9]", "p_fr_cap_al_obt_res_2[8]", "p_fr_cap_al_obt_res_2[7]", "p_fr_cap_al_obt_res_2[6]", "p_fr_cap_al_obt_res_2[5]", "p_fr_cap_al_obt_res_2[4]", "p_ind_cap_out_ratio_1",]
    influencers_1901_rms    = ["nr_resources_init", "industrial_capital_init", "service_capital_init", "agr_inp_init", "pot_arable_land_init", "pop2_init", "pop1_init", "arable_land_init", "pop3_init", "pop4_init", "pers_pollution_init", "urban_ind_land_init", "land_fertility_init", "ppoll_tech_init", "res_tech_init", "perc_food_ratio_init", "labor_util_fr_del_init", "yield_tech_init"]

    # 2100
    influencers_2100_rms    = ["p_fioa_cons_const_1", "p_ind_cap_out_ratio_1", "p_avg_life_ind_cap_1", "life_expect_norm", "reproductive_lifetime", "p_serv_cap_out_ratio_1", "land_fr_harvested", "inherent_land_fert", "p_land_yield_fact_1", "nr_resources_init", "des_compl_fam_size_norm", "subsist_food_pc", "pot_arable_land_init", "max_tot_fert_norm", "p_nr_res_use_fact_1", "p_avg_life_serv_cap_1", "pot_arable_land_tot", "industrial_capital_init", "pop2_init", "arable_land_init", "land_fertility_init", "pop1_init", "service_capital_init", "processing_loss", "lifet_perc_del", "income_expect_avg_time", "p_ppoll_gen_fact_1", "avg_life_land_norm", "assim_half_life_1970", "ppoll_in_1970", "p_avg_life_agr_inp_1", "social_discount", "social_adj_del", "ind_mtl_toxic_index", "ind_mtl_emiss_fact", "frac_res_pers_mtl", "agr_mtl_toxic_index", "fr_agr_inp_pers_mtl", "ppoll_trans_del", "hlth_serv_impact_del", "agr_inp_init", "pop3_init", "labor_util_fr_del_init", "labor_force_partic", "urban_ind_land_init", "urb_ind_land_dev_time", "food_short_perc_del", "pop4_init", "perc_food_ratio_init", "labor_util_fr_del_time", "pers_pollution_init", "tech_dev_del_TDD", "yield_tech_init", "res_tech_init", "ppoll_tech_init"]
    noninfluencers_2100_rms = ["t_air_poll_time", "des_food_ratio_dfr", "t_fcaor_time", "des_res_use_rt_DNRUR", "t_fert_cont_eff_time", "ind_out_in_1970", "ind_out_pc_des", "t_ind_equil_time", "t_land_life_time", "t_policy_year", "p_avg_life_agr_inp_2", "t_pop_equil_time", "t_zero_pop_grow_time", "des_ppoll_index_DPOLX", "p_fr_cap_al_obt_res_2[5]", "p_avg_life_ind_cap_2", "p_fr_cap_al_obt_res_2[6]", "p_fr_cap_al_obt_res_2[7]", "p_fr_cap_al_obt_res_2[8]", "p_fr_cap_al_obt_res_2[9]", "p_fr_cap_al_obt_res_2[10]", "p_fr_cap_al_obt_res_2[11]", "p_fr_cap_al_obt_res_2[4]", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[2]", "p_fr_cap_al_obt_res_2[1]", "p_ppoll_tech_chg_mlt[1]", "p_ppoll_tech_chg_mlt[2]", "p_ppoll_tech_chg_mlt[3]", "p_ppoll_tech_chg_mlt[4]", "p_res_tech_chg_mlt[1]", "p_res_tech_chg_mlt[2]", "p_res_tech_chg_mlt[3]", "p_res_tech_chg_mlt[4]", "p_fioa_cons_const_2", "p_serv_cap_out_ratio_2", "p_yield_tech_chg_mlt[1]", "p_yield_tech_chg_mlt[2]", "p_yield_tech_chg_mlt[3]", "p_yield_tech_chg_mlt[4]", "p_avg_life_serv_cap_2"]
    # Put them into dict so I don't have to breakdown the "for loop"
    influencers_and_noninfluencers_dict = {
        "1901": {"noninfluencers":noninfluencers_1901_rms,
               "influencers": influencers_1901_rms,
               },
        "2100": {"noninfluencers":noninfluencers_2100_rms,
               "influencers": influencers_2100_rms,
               }
    }
    for year in ["1901","2100"]:
        influencers = influencers_and_noninfluencers_dict[year]["influencers"]
        noninfluencers = influencers_and_noninfluencers_dict[year]["noninfluencers"]
        input_matrix_path = "resource/paramVarSensMatrix/empiricalSens/"+year+"/root_mean_squares_perturbed_5percent_From1900To"+year+".csv"
        # Plot influencers
        plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using Root Mean Square formula for the year "+year+". Only parameters that have effect."
        plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_rootMeanSquares_"+year+"_onlyInfluencers_heatmap")
        os.makedirs(plot_folder_path)
        plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=influencers)
        # Plot noninfluencers
        # plot_title = "Empirical Parameter Sensitivity for "+year+" for World3-Modelica\nSensitivity calculated using Root Mean Square formula for the year "+year+". Only parameters that have NO effect."
        # plot_folder_path = os.path.join(base_path,"omEmpiricalParamSens_rootMeanSquares_"+year+"_onlyNonnfluencers_heatmap")
        # os.makedirs(plot_folder_path)
        # plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=noninfluencers)
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
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Vanilla World3-Modelica\nAll differentiable variables but only parameters that have at least one influence according to  IDAsens, NOT including extra differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=influencers_params)
# Heatmap of vanilla matrix for 1901 only including non-influencer params
def omTheoParamSens_1901_VanillaW3_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path):
    nonInfluencers_params = ['p_fr_cap_al_obt_res_2[10]','p_ppoll_tech_chg_mlt[3]','ind_out_pc_des','p_ppoll_tech_chg_mlt[2]','labor_util_fr_del_time','service_capital_init','labor_force_partic','p_res_tech_chg_mlt[2]','social_discount','inherent_land_fert','pop1_init','p_avg_life_serv_cap_2','food_short_perc_del','t_zero_pop_grow_time','t_policy_year','pot_arable_land_tot','t_ind_equil_time','des_compl_fam_size_norm','des_food_ratio_dfr','p_fr_cap_al_obt_res_2[6]','ind_out_in_1970','p_serv_cap_out_ratio_1','pers_pollution_init','p_fr_cap_al_obt_res_2[5]','res_tech_init','des_ppoll_index_DPOLX','p_fr_cap_al_obt_res_2[11]','t_pop_equil_time','p_fr_cap_al_obt_res_2[9]','pot_arable_land_init','reproductive_lifetime','p_ppoll_gen_fact_1','tech_dev_del_TDD','t_land_life_time','yield_tech_init','t_fert_cont_eff_time','p_ppoll_tech_chg_mlt[4]','p_fr_cap_al_obt_res_2[2]','labor_util_fr_del_init','p_ind_cap_out_ratio_1','fr_agr_inp_pers_mtl','frac_res_pers_mtl','social_adj_del','des_res_use_rt_DNRUR','income_expect_avg_time','p_fr_cap_al_obt_res_2[1]','p_res_tech_chg_mlt[1]','subsist_food_pc','p_yield_tech_chg_mlt[1]','industrial_capital_init','p_ppoll_tech_chg_mlt[1]','land_fertility_init','pop2_init','t_fcaor_time','ppoll_tech_init','urban_ind_land_init','ppoll_in_1970','p_fr_cap_al_obt_res_2[8]','p_land_yield_fact_1','hlth_serv_impact_del','urb_ind_land_dev_time','land_fr_harvested','p_yield_tech_chg_mlt[2]','pop3_init','p_res_tech_chg_mlt[3]','p_fioa_cons_const_2','pop4_init','p_serv_cap_out_ratio_2','avg_life_land_norm','p_nr_res_use_fact_1','max_tot_fert_norm','p_fr_cap_al_obt_res_2[7]','p_avg_life_serv_cap_1','t_air_poll_time','nr_resources_init','p_res_tech_chg_mlt[4]','p_avg_life_agr_inp_1','p_avg_life_ind_cap_2','p_yield_tech_chg_mlt[3]','p_fioa_cons_const_1']
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_vanilla.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901 for Vanilla World3-Modelica\nAll differentiable variables but only parameters that have NO influence from IDAsens, NOT including extra differentiable population var"
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
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901\nAll original differentiable variables plus extra differentiable population var. Only parameters that have effect."
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=influencers_params)
# Heatmap of vanilla matrix for 1901 only including non-influencer params
def omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveNoInfluenceIn1901_heatmap(base_path):
    nonInfluencers_params = ['p_fr_cap_al_obt_res_2[10]','p_ppoll_tech_chg_mlt[3]','ind_out_pc_des','p_ppoll_tech_chg_mlt[2]','labor_util_fr_del_time','service_capital_init','labor_force_partic','p_res_tech_chg_mlt[2]','social_discount','inherent_land_fert','pop1_init','p_avg_life_serv_cap_2','food_short_perc_del','t_zero_pop_grow_time','t_policy_year','pot_arable_land_tot','t_ind_equil_time','des_compl_fam_size_norm','des_food_ratio_dfr','p_fr_cap_al_obt_res_2[6]','ind_out_in_1970','p_serv_cap_out_ratio_1','pers_pollution_init','p_fr_cap_al_obt_res_2[5]','res_tech_init','des_ppoll_index_DPOLX','p_fr_cap_al_obt_res_2[11]','t_pop_equil_time','p_fr_cap_al_obt_res_2[9]','pot_arable_land_init','reproductive_lifetime','p_ppoll_gen_fact_1','tech_dev_del_TDD','t_land_life_time','yield_tech_init','t_fert_cont_eff_time','p_ppoll_tech_chg_mlt[4]','p_fr_cap_al_obt_res_2[2]','labor_util_fr_del_init','p_ind_cap_out_ratio_1','fr_agr_inp_pers_mtl','frac_res_pers_mtl','social_adj_del','des_res_use_rt_DNRUR','income_expect_avg_time','p_fr_cap_al_obt_res_2[1]','p_res_tech_chg_mlt[1]','subsist_food_pc','p_yield_tech_chg_mlt[1]','industrial_capital_init','p_ppoll_tech_chg_mlt[1]','land_fertility_init','pop2_init','t_fcaor_time','ppoll_tech_init','urban_ind_land_init','ppoll_in_1970','p_fr_cap_al_obt_res_2[8]','p_land_yield_fact_1','hlth_serv_impact_del','urb_ind_land_dev_time','land_fr_harvested','p_yield_tech_chg_mlt[2]','pop3_init','p_res_tech_chg_mlt[3]','p_fioa_cons_const_2','pop4_init','p_serv_cap_out_ratio_2','avg_life_land_norm','p_nr_res_use_fact_1','max_tot_fert_norm','p_fr_cap_al_obt_res_2[7]','p_avg_life_serv_cap_1','t_air_poll_time','nr_resources_init','p_res_tech_chg_mlt[4]','p_avg_life_agr_inp_1','p_avg_life_ind_cap_2','p_yield_tech_chg_mlt[3]','p_fioa_cons_const_1']
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901\nAll variables but only parameters that have NO influence from IDAsens, including extra differentiable population var."
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_PopStateVarNew_onlyParamsThatHaveNoInfluenceIn1901_heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,rows_to_plot=nonInfluencers_params)
# All params and vars for 1901 sens
def omTheoParamSens_1901_PopStateVarNew_all_Heatmap(base_path):
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901\nAll variables and parameters from Sensitivity Analysis, including new differentiable population var"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_all_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title)

# Workpackage1 params and vars for 1901 sens
def omTheoParamSens_1901_PopStateVarNew_onlyWorkPackage1ParamsAndVars_Heatmap(base_path):
    workpackage1_params = ["agr_mtl_toxic_index", "assim_half_life_1970", "ind_mtl_emiss_fact", "ind_mtl_toxic_index", "life_expect_norm", "p_avg_life_agr_inp_2", "p_avg_life_ind_cap_1", "p_fr_cap_al_obt_res_2[3]", "p_fr_cap_al_obt_res_2[4]"]
    workpackage1_vars = [ "Arable_Land_Dynamics1.Arable_Land.Integrator1.y", "Arable_Land_Dynamics1.Pot_Arable_Land.Integrator1.y", "Food_Production1.Agr_Inp.Integrator1.y"]
    input_matrix_path = "resource/paramVarSensMatrix/theoSens/1901/paramVarMatrix_TheoParamSens_1901_diffPopNewVar.csv"
    plot_title = "OpenModelica Theoretical Parameter Sensitivity for 1901\nOnly the variables and parameters studied in WorkPackage 1"
    plot_folder_path = os.path.join(base_path,"omTheoParamSens_1901_onlyWorkPackage1ParamsAndVars_Heatmap")
    os.makedirs(plot_folder_path)
    plotting.plot_heatmap.readCSVMatrixAndPlotHeatmap(input_matrix_path,plot_folder_path,plot_title,columns_to_plot=workpackage1_vars,rows_to_plot=workpackage1_params)

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
