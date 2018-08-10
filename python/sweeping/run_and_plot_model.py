# This is the main script for configuring, running and plotting a OpenModelica Sweep
import os
import re
import platform
import logging  # en reemplazo de los prints

logger = logging.getLogger("--Run and Plot OpenModelica--")  # un logger especifico para este modulo
# My imports
import plotting.plot_csv as plot_csv
import settings.gral_settings as gral_settings
import readme_writer.readme_writer as readme_writer
import filesystem.files_aux
import modelica_interface.run_omc as run_omc


def createSweepRunAndPlotForModelInfo(mos_script_factory_inst, plot_vars, iterations, output_folder_path,
                                      sweep_value_formula_str, csv_file_name_python_skeleton,
                                      csv_file_name_modelica_skeleton, plot_std_run, fixed_params_str):
    output_mos_path = os.path.join(output_folder_path, gral_settings.mos_script_filename)
    # EL scripting de modelica se rompe con la backslash (aunque estemos en windows). Hay que mandar la de unix nomas:
    output_mos_path = output_mos_path.replace("\\", "/")
    csv_file_name_modelica = csv_file_name_modelica_skeleton.format(i_name="i")
    mos_script_factory_inst.setSetting("csv_file_name_modelica", csv_file_name_modelica)
    # mos_script_factory_inst.setSetting("plot_vars",plot_vars)
    mos_script_factory_inst.setSetting("iterations", iterations)
    mos_script_factory_inst.setSetting("sweep_value_formula_str", sweep_value_formula_str)
    mos_script_factory_inst.setSetting("output_mos_path", output_mos_path)
    mos_script_factory_inst.createMosScript()  # argument-less method for now
    writeRunLog(mos_script_factory_inst.initializedSettings(),
                os.path.join(output_folder_path, gral_settings.omc_creation_settings_filename))
    run_omc.runMosScript(output_mos_path)
    plots_folder_path = os.path.join(output_folder_path, "plots")
    os.makedirs(plots_folder_path)
    sweeping_vars = mos_script_factory_inst.initializedSettings()["sweep_vars"]
    sweeping_info = sweepingInfoPerIteration(mos_script_factory_inst.initializedSettings(),
                                             csv_file_name_python_skeleton)
    model_name_only = mos_script_factory_inst.initializedSettings()["model_name"].split(".")[-1]
    plot_csv.plotVarsFromSweepingInfo(plot_vars, model_name_only, sweeping_info, plots_folder_path, plot_std_run,
                                      fixed_params_str)
    readme_path = os.path.join(output_folder_path, gral_settings.readme_filename)
    readme_writer.writeReadme(readme_path, sweeping_info)


def sweepingInfoPerIteration(settings, csv_file_name_python_skeleton):
    iterations = settings["iterations"]
    sweep_formula = settings["sweep_value_formula_str"]  # only variable should be i
    model_name = settings["model_name"]
    output_mos_path = settings["output_mos_path"]
    run_root_folder = os.path.dirname(output_mos_path)
    sweep_vars = settings["sweep_vars"]
    fixed_params = settings["fixed_params"]
    per_iter_info_dict = {}
    for i in range(0, iterations):
        iter_dict = {}
        csv_name = csv_file_name_python_skeleton.format(**{"model_name": model_name, "i_str": str(i)})
        csv_path = os.path.join(run_root_folder, csv_name)
        iter_dict["file_path"] = csv_path
        iter_dict["sweep_value"] = eval(sweep_formula)  # this eval uses i!!!
        per_iter_info_dict[i] = iter_dict
    sweeping_info_dict = {"per_iter_info_dict": per_iter_info_dict, "sweep_vars": sweep_vars,
                          "fixed_params": fixed_params}
    return sweeping_info_dict


def writeRunLog(run_settings_dict, output_path):
    intro_str = """The whole "create mos, run it and plot it" script was run with the following settings""" + "\n"
    format_explanation_str = """<setting_name>:\n   <setting_value>""" + "\n"
    all_settings = []
    for setting_name, setting_value in run_settings_dict.items():
        setting_str = """{setting_name}:\n {setting_value}""".format(setting_name=setting_name,
                                                                     setting_value=setting_value)
        all_settings.append(setting_str)
    all_settings_str = "\n".join(all_settings)
    final_str = intro_str + format_explanation_str + "\n" + all_settings_str
    filesystem.files_aux.writeStrToFile(final_str, output_path)
    return 0
