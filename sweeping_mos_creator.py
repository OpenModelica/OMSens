def main():
    # model_name = "SystemDynamics.WorldDynamics.World3.Scenario_1"
    model_name = "BouncingBall"
    mos_kwargs = {
        "input_path": "BouncingBall.mo",
        # "input_path": "package.mo",
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
        }
    final_str = mos_skeleton_str.format(**mos_kwargs)
    output_mos_path = "bball_sweep.mos"
    # output_mos_path = "world3_sweep.mos"
    writeStrToFile(final_str,output_mos_path)

    #CREAR EL SH QUE BORRA TODO
    writeStrToFile("rm {0}*{{.c,.o,.h,.makefile,.log,.libs,.xml,.json}}".format(model_name), "rm_everything.sh")



def writeStrToFile(str_,file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0


mos_skeleton_str = \
"""
// load the file
loadFile("{input_path}");
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
  plot({plot_var},fileName=file_name_i,externalWindow=true);
end for;

//PARA BORRAR LOS ARCHIVOS TEMPORALES RESULTANTES(limpia la carpeta un poco)
system("bash rm_everything.sh");
//system("rm rm_everything.sh"); //si borro el borrador, despues de correr el .mos de nuevo no tengo forma de borrarlo.
"""



if __name__ == "__main__":
    main()
