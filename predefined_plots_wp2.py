#Standard
import os
import sys
import logging #en reemplazo de los prints
logger = logging.getLogger("--Predefined Plotting script for Wp2 results--") #un logger especifico para este modulo
#Mine
import filesystem.files_aux
import plotting.plot_csv
def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # to show logging info into STDOUT
    base_path = filesystem.files_aux.makeOutputPath("predefined_plots")
    plotRelativeTop12FromPreranResults(base_path)
    plotRMSTop12FromPreranResults(base_path)
    plotRMSTop12AndRelativeTop12FromPreranResults(base_path)
def plotRMSTop12AndRelativeTop12FromPreranResults(base_path):
    plot_folder_path = os.path.join(base_path,"rmsTop12vsRelativeTop12Experimentation")
    os.makedirs(plot_folder_path)
    # Arguments:
    plot_title = "RMS Top12 vs Relative Top12 vs Standard run"
    plot_subtitle= "Plot comparison of RMS and Relative experimentation and the Standard run"
    plus_5_percent_params = "max_tot_fert_norm,p_fioa_cons_const_1,p_ind_cap_out_ratio_1,\np_serv_cap_out_ratio_1,life_expect_norm,des_compl_fam_size_norm"
    minus_5_percent_params = "p_land_yield_fact_1, reproductive_lifetime, subsist_food_pc,n p_avg_life_ind_cap_1, land_fr_harvested, inherent_land_fert"
    plot_footer = ""
    x_range = [1900,2500]
    csvs_path_label_pair_list = [("/home/adanos/Documents/tesis/prog/w3_contrato_suecia/workpackage2/results/empirical_analysis/5_percent/6_most_positive_up_6_most_negative_down/6_most_absolutevalue_sensitive_perturbation.csv",
                                  "12_params_perturbed_relative"),
                                 ("/home/adanos/Documents/tesis/prog/w3_contrato_suecia/workpackage2/results/empirical_analysis/5_percent/rms_6_most_positive_up_6_most_negative_down/12_most_rootmeansquares_special_assignment_5percent.csv",
                                  "12_params_perturbed_RMS")]
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
      "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
    }
    plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)

def plotRMSTop12FromPreranResults(base_path):
    plot_folder_path = os.path.join(base_path,"rmsTop12Experimentation")
    os.makedirs(plot_folder_path)
    # Arguments:
    plot_title = "Perturbation of Top 12 Parameters RMS"
    plot_subtitle= "Top 6 positive influence parameters set to 105% and top 6 negative influence parameters set to 95%"
    plus_5_percent_params = "max_tot_fert_norm,p_fioa_cons_const_1,p_ind_cap_out_ratio_1,\np_serv_cap_out_ratio_1,life_expect_norm,des_compl_fam_size_norm"
    minus_5_percent_params = "p_land_yield_fact_1, reproductive_lifetime, subsist_food_pc,\nn p_avg_life_ind_cap_1, land_fr_harvested, inherent_land_fert"
    plot_footer = "Parameters perturbed:\n-5%:{minus_5_percent_params}.\n+5%:{plus_5_percent_params}.".format(minus_5_percent_params=minus_5_percent_params,plus_5_percent_params=plus_5_percent_params)
    x_range = [1900,2100]
    csvs_path_label_pair_list = [("/home/adanos/Documents/tesis/prog/w3_contrato_suecia/workpackage2/results/empirical_analysis/5_percent/rms_6_most_positive_up_6_most_negative_down/12_most_rootmeansquares_special_assignment_5percent.csv",
                                  "12_params_perturbed_RMS")]
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
      "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
    }
    plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)

def plotRelativeTop12FromPreranResults(base_path):
    plot_folder_path = os.path.join(base_path,"relativeTop12Experimentation")
    os.makedirs(plot_folder_path)
    # Arguments:
    plot_title = "Perturbation of Top 12 Parameters Relative"
    plot_subtitle= "Top 6 positive influence parameters set to 105% and top 6 negative influence parameters set to 95%"
    plus_5_percent_params = "max_tot_fert_norm,p_fioa_cons_const_1,p_ind_cap_out_ratio_1,\np_serv_cap_out_ratio_1,life_expect_norm,des_compl_fam_size_norm"
    minus_5_percent_params = "industrial_capital_init,p_land_yield_fact_1,p_nr_res_use_fact_1,\nreproductive_lifetime,subsist_food_pc,p_avg_life_ind_cap_1"
    plot_footer = "Parameters perturbed:\n-5%:{minus_5_percent_params}.\n+5%:{plus_5_percent_params}.".format(minus_5_percent_params=minus_5_percent_params,plus_5_percent_params=plus_5_percent_params)
    x_range = [1900,2100]
    csvs_path_label_pair_list = [("/home/adanos/Documents/tesis/prog/w3_contrato_suecia/workpackage2/results/empirical_analysis/5_percent/6_most_positive_up_6_most_negative_down/6_most_absolutevalue_sensitive_perturbation.csv",
                                  "12_params_perturbed_relative")]
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
      "vars_list":["population"], # only one var plottable for now (needs a variable amount of inputs)
    }
    plotting.plot_csv.multipleCSVsAndVarsSimplePlot(**plotter_kwargs)

# FIRST EXECUTABLE CODE:
if __name__ == "__main__":
    main()
