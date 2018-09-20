# Std
import numpy
from scipy.optimize import minimize
import pybobyqa

# This project
import modelica_interface.build_model as build_model
import filesystem.files_aux as files_aux


def main():
    # Model information
    model_name = "SystemDynamics.WorldDynamics.World3.Scenario_1"
    model_file_path = files_aux.moFilePathFromJSONMoPath("resource/sys_dyn/pw_fix/SystemDynamics/package.mo")
    start_time = 1900
    stop_time = 2100
    param_names = ["max_tot_fert_norm", "p_fioa_cons_const_1", "p_ind_cap_out_ratio_1",
                   "p_serv_cap_out_ratio_1", "life_expect_norm", "des_compl_fam_size_norm",
                   "industrial_capital_init", "p_land_yield_fact_1", "p_nr_res_use_fact_1",
                   "reproductive_lifetime", "subsist_food_pc", "p_avg_life_ind_cap_1"]
    target_var_name = "population"
    x0 =  [12.0, 0.43, 3.0, 1.0, 28.0, 3.8, 210000000000.0, 1.0, 1.0, 30.0, 230.0, 14.0]
    dest_folder_path = files_aux.makeOutputPath("vectorial_analysis")
    fun = createObjectiveFunctionForModel(model_name, start_time, stop_time, model_file_path, param_names,
                                          target_var_name, dest_folder_path)
    bnds = [[x*0.95,x*1.05] for x in x0]
    res = minimize(fun, x0, method='L-BFGS-B', bounds=bnds)
    print(res)

# CURVI VERSION, NEEDS TO BE ADAPTED TO ABOVE FORMAT WITH BNDS, EPSILON, ETC
# # Std
# import numpy
# # Project
# import fortran_interface.curvif_simplified as curvif_simplified
# x0 = numpy.array([1,1])
# obj_func = lambda x: -(x[0] + x[1])
# epsilon = 0.001
# x_opt,f_opt = curvif_simplified.curvif_simplified(x0,obj_func,epsilon)
# print("x_opt:",x_opt)
# print("f_opt:",f_opt)


def createObjectiveFunctionForModel(model_name, start_time, stop_time, model_file_path, param_names, target_var_name,
                                    build_folder_path):
    # Initialize builder
    model_builder = build_model.ModelicaModelBuilder(model_name, start_time, stop_time, model_file_path)
    # Build model
    compiled_model = model_builder.buildToFolderPath(build_folder_path)

    def objectiveFunction(params_vals):
        # Set the values for each respective parameter
        for i in range(len(param_names)):
            p_name = param_names[i]
            p_val = params_vals[i]
            compiled_model.setParameterStartValue(p_name, p_val)
        # Run the simulation
        var_val = compiled_model.quickSimulate(target_var_name)
        return var_val

    return objectiveFunction


if __name__ == "__main__":
    main()
