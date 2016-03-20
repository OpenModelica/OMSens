def main():
    # model_name = "SystemDynamics.WorldDynamics.World3.Scenario_1"
    model_name = "BouncingBall"
    mos_kwargs = {
        "mo_file": "BouncingBall.mo",
        # "mo_file": "package.mo",
        "model_name": model_name, #Lo pongo aparte porque lo uso en el rm_everything
        "sweep_var": "e",
        # "sweep_var": "life_expect_norm",
        "plot_var": "h",
        # "plot_var": "nr_resources",
        "initial": 0.7,
        # "initial": 25,
        "increment": 0.1,
        # "increment": 1,
        "iterations": 3,
        # "iterations": 10,
        "output_mos_path": "bball_sweep.mos"
        }
    # output_mos_path = "world3_sweep.mos"
    createMos(**mos_kwargs)
def createMos(mo_file,model_name,sweep_var,plot_var,initial,increment,iterations,output_mos_path):
    final_str = mos_skeleton_str.format(mo_file=mo_file,model_name=model_name,sweep_var=sweep_var,plot_var=plot_var,initial=initial,increment=increment,iterations=iterations)
    writeStrToFile(final_str,output_mos_path)



def writeStrToFile(str_,file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0


mos_skeleton_str = \
"""
// load the file
loadFile("{mo_file}");
getErrorString();
// build the model once
//buildModel({model_name});
buildModel({model_name}, outputFormat="csv");
getErrorString();
for i in 1:{iterations} loop
  // BouncingBall_init.xml file will be generated because of buildModel call above.
  // We update the parameter h start value from 0.7 to "0.7 + i".
  value := {initial} + i*{increment};
  setInitXmlStartValue("{model_name}_init.xml", "{sweep_var}", String(value) , "{model_name}_init.xml");
  getErrorString();
  // call the generated simulation code to produce a result file BouncingBall%i%_res.mat
  file_name_i := "{model_name}_" + String(i) + "_res.csv";
  //system("{model_name}.exe -r="+file_name_i);
  system("./{model_name} -r="+file_name_i);
  getErrorString();
  //plot({plot_var},fileName=file_name_i,externalWindow=true);
end for;
"""



if __name__ == "__main__":
    main()
