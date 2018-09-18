# Std
from scipy.optimize import minimize

# This project
import modelica_interface.build_model as build_model
import filesystem.files_aux as files_aux

def main():
    # Model information
    model_name = "ModelWithVariousParams"
    model_file_path = files_aux.moFilePathFromJSONMoPath("resource/ModelWithVariousParams.mo")
    start_time = 0
    stop_time = 10
    param_names = ["realParam1", "realParam2", "realParam3"]
    target_var_name = "outvar1"
    dest_folder_path = files_aux.makeOutputPath("vectorial_analysis")
    fun = createObjectiveFunctionForModel(model_name, start_time, stop_time, model_file_path, param_names, target_var_name, dest_folder_path)
    bnds = [[None, None], [None, None], [None,None]]
    x0 = [1.121, 1.122, 1.23]
    res = minimize(fun, x0, method='L-BFGS-B', bounds=bnds)
    print(res)

def createObjectiveFunctionForModel(model_name, start_time, stop_time, model_file_path, param_names, target_var_name, build_folder_path):
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

