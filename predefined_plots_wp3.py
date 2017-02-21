#Standard
import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--Predefined Plotting script for Wp3 results--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux
import plotting.plot_csv
def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # to show logging info into STDOUT
    base_path = filesystem.files_aux.makeOutputPath("predefined_plots")
    # nrResInitCurviVsZXPOWL_curviNoBounds_population(base_path)
    top12FromRelative_curvi5Perc_populationVSpopAndhwi(base_path)
    # top12FromRelative_curvi3Perc_populationVShwi(base_path)    # no encontré el only pop.
    # onlyMeasurableInits_curvi3Perc_population(base_path)       # me parece que con el plot de multiparam sweep basta. Con quién lo compararíamos acá para justificar su presencia en este archivo?
#    # top12FromRelative_WP2vscurvi5Perc_populationVShwi(base_path) ## <--- PARA ESTE TODAVÍA HAY QUE HACER EL MULTIPARAM SWEEP
    sys.exit(0)

# BORRAR:
    # plotRelativeTop12FromPreranResults(base_path)
    # plotRMSTop12FromPreranResults(base_path)
    # plotRMSTop12AndRelativeTop12FromPreranResults(base_path)
# BORRAR^
def nrResInitCurviVsZXPOWL_curviNoBounds_population(base_path):
    # Make base dir
    plot_folder_path = os.path.join(base_path,"nrResInitCurviVsZXPOWL_curviNoBounds")
    os.makedirs(plot_folder_path)
    # Make 1900 to 2500 dir
    plot_folder_path_1900to2500 = os.path.join(plot_folder_path,"1900to2500")
    os.makedirs(plot_folder_path_1900to2500)
    # Make 2090 to 2110 dir
    plot_folder_path_2090to2110 = os.path.join(plot_folder_path,"2090to2110")
    os.makedirs(plot_folder_path_2090to2110)
    # Arguments:
    plot_title = "Non Renewable Resources: curvi vs zxpowl"
    plot_subtitle= "Plot comparison of the optimization results of curvi and zxpowl"
    nrResInit_curvi = "1322956409277.25 [+32%]"
    nrResInit_zxpowl = "1331113420897.75 [+33%]"
    plot_footer = "Parameter perturbed: {params_perturbed}\ncurvi result:{curvi_result}.\nzxpowl result:{zxpowl_result}.".format(params_perturbed="nr_resources_init",curvi_result=nrResInit_curvi,zxpowl_result=nrResInit_zxpowl)
    x_range = [1900,2500]
    csvs_path_label_pair_list = [("resource/wp3Simus/nrResInitNoBoundsCurvi3PercNoSweepOptimizePop/run/iter_0.csv",
                                  "population:curvi"),
                                 ( "resource/wp3Simus/nrResInitNoBoundsZXPWLNoSweepOptimizePop/run/iter_0.csv",
                                  "population:zxpowl")]
    #Kwargs definition
    # 1900 to 2500 kwargs:
    plotter_kwargs = {
      "plot_title": plot_title,
      "subtitle": plot_subtitle,
      "footer": plot_footer,
      "csvs_path_label_pair_list": csvs_path_label_pair_list,
      "x_range": x_range,
      "output_folder_path": plot_folder_path_1900to2500,
      "extra_ticks": [],
      "include_stdrun": True,
      "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
    }
    plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)
    # 2090 to 2110 kwargs:
    plotter_kwargs = {
      "plot_title": plot_title,
      "subtitle": plot_subtitle,
      "footer": plot_footer,
      "csvs_path_label_pair_list": csvs_path_label_pair_list,
      "x_range": [2090,2110],
      "output_folder_path": plot_folder_path_2090to2110,
      "extra_ticks": [],
      "include_stdrun": True,
      "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
    }
    plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)
def top12FromRelative_curvi5Perc_populationVSpopAndhwi(base_path):
    # Make base dir
    plot_folder_path = os.path.join(base_path,"top12FromRelative_curvi5Perc")
    os.makedirs(plot_folder_path)
    # Arguments:
    plot_title = "Top 12 From Relative senstivity index: curvi 5% only pop vs pop and hwi"
    plot_subtitle= "Plot comparison of the optimization results of curvi with 5% bounds using only population as optimization target vs using population/1E10 + human_welfare_index"
    params_perturbed = "max_tot_fert_norm (0), p_fioa_cons_const_1 (1), p_ind_cap_out_ratio_1 (2), p_serv_cap_out_ratio_1 (3), life_expect_norm (4), des_compl_fam_size_norm (5), industrial_capital_init (6), p_land_yield_fact_1 (7), p_nr_res_use_fact_1 (8), reproductive_lifetime (9), subsist_food_pc (10), p_avg_life_ind_cap_1 (11)"
    top12_onlyPop = "(0)=12.60 [+4%] | (1)=0.45 [+4%] | (2)=3.15 [+4%] | (3)=1.05 [+4%] | (4)=29.40 [+4%] | (5)=3.99 [+4%] | (6)=199500000000.00 [-5%] | (7)=1.05 [+4%] | (8)=0.95 [-5%] | (9)=28.50 [-5%] | (10)=218.50 [-5%] | (11)=14.70 [+4%]"
    top12_popAndHWI = "(0)=11.41 [-4%] | (1)=0.45 [+4%] | (2)=3.15 [+4%] | (3)=1.04 [+4%] | (4)=29.31 [+4%] | (5)=3.86 [+1%] | (6)=199561334891.51 [-4%] | (7)=0.99 [-0%] | (8)=1.05 [+4%] | (9)=28.62 [-4%] | (10)=220.20 [-4%] | (11)=14.29 [+2%]"
    plot_footer = "Parameter perturbed: {params_perturbed}\noptimizing only pop:{first_result}.\noptimizing pop/1e10 + hwi:{second_result}.".format(params_perturbed=params_perturbed,first_result=top12_onlyPop,second_result=top12_popAndHWI)
    x_range = [1900,2500]
    csvs_path_label_pair_list = [("resource/wp3Simus/reltop12Curvi5percNoSweepOptimizePop/reltop12Curvi5percNoSweepOptimizePop.csv",
                                 "optimizing only pop"),
                                ("resource/wp3Simus/reltop12Curvi5PercNoSweepOptimizePopAndHWI/reltop12Curvi5PercNoSweepOptimizePopAndHWI.csv",
                                 "optimizing pop/1e10 + hwi")]
    #Kwargs definition
    plotter_kwargs = {
      "plot_title": plot_title,
      "subtitle": plot_subtitle,
      "footer": plot_footer,
      "csvs_path_label_pair_list": csvs_path_label_pair_list,
      "x_range": x_range,
      "output_folder_path": plot_folder_path,
      "extra_ticks": [],
      "include_stdrun": True,
      "vars_list_pairs":[("population","human_welfare_index")],
    }
    plotting.plot_csv.twoVarsMultipleCSVsPlot(**plotter_kwargs)
#
# def plotRMSTop12FromPreranResults(base_path):
#     plot_folder_path = os.path.join(base_path,"rmsTop12Experimentation")
#     os.makedirs(plot_folder_path)
#     # Arguments:
#     plot_title = "Perturbation of Top 12 Parameters RMS"
#     plot_subtitle= "Top 6 positive influence parameters set to 105% and top 6 negative influence parameters set to 95%"
#     plus_5_percent_params = "max_tot_fert_norm,p_fioa_cons_const_1,p_ind_cap_out_ratio_1,\np_serv_cap_out_ratio_1,life_expect_norm,des_compl_fam_size_norm"
#     minus_5_percent_params = "p_land_yield_fact_1, reproductive_lifetime, subsist_food_pc,\nn p_avg_life_ind_cap_1, land_fr_harvested, inherent_land_fert"
#     plot_footer = "Parameters perturbed:\n-5%:{minus_5_percent_params}.\n+5%:{plus_5_percent_params}.".format(minus_5_percent_params=minus_5_percent_params,plus_5_percent_params=plus_5_percent_params)
#     x_range = [1900,2100]
#     csvs_path_label_pair_list = [("/home/adanos/Documents/tesis/prog/w3_contrato_suecia/workpackage2/results/empirical_analysis/5_percent/rms_6_most_positive_up_6_most_negative_down/12_most_rootmeansquares_special_assignment_5percent.csv",
#                                   "12_params_perturbed_RMS")]
#     #Kwargs definition
#     plotter_kwargs = {
#       "plot_title": plot_title,
#       "subtitle": plot_subtitle,
#       "footer": plot_footer,
#       "csvs_path_label_pair_list": csvs_path_label_pair_list,
#       "x_range": x_range,
#       "output_folder_path": plot_folder_path,
#       "extra_ticks": [],
#       "include_stdrun": True,
#       "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
#     }
#     plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)
#
# def plotRelativeTop12FromPreranResults(base_path):
#     plot_folder_path = os.path.join(base_path,"relativeTop12Experimentation")
#     os.makedirs(plot_folder_path)
#     # Arguments:
#     plot_title = "Perturbation of Top 12 Parameters Relative"
#     plot_subtitle= "Top 6 positive influence parameters set to 105% and top 6 negative influence parameters set to 95%"
#     plus_5_percent_params = "max_tot_fert_norm,p_fioa_cons_const_1,p_ind_cap_out_ratio_1,\np_serv_cap_out_ratio_1,life_expect_norm,des_compl_fam_size_norm"
#     minus_5_percent_params = "industrial_capital_init,p_land_yield_fact_1,p_nr_res_use_fact_1,\nreproductive_lifetime,subsist_food_pc,p_avg_life_ind_cap_1"
#     plot_footer = "Parameters perturbed:\n-5%:{minus_5_percent_params}.\n+5%:{plus_5_percent_params}.".format(minus_5_percent_params=minus_5_percent_params,plus_5_percent_params=plus_5_percent_params)
#     x_range = [1900,2100]
#     csvs_path_label_pair_list = [("/home/adanos/Documents/tesis/prog/w3_contrato_suecia/workpackage2/results/empirical_analysis/5_percent/6_most_positive_up_6_most_negative_down/6_most_absolutevalue_sensitive_perturbation.csv",
#                                   "12_params_perturbed_relative")]
#     #Kwargs definition
#     plotter_kwargs = {
#       "plot_title": plot_title,
#       "subtitle": plot_subtitle,
#       "footer": plot_footer,
#       "csvs_path_label_pair_list": csvs_path_label_pair_list,
#       "x_range": x_range,
#       "output_folder_path": plot_folder_path,
#       "extra_ticks": [],
#       "include_stdrun": True,
#       "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
#     }
#     plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)
#
# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
