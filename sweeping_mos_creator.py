def main():
    pass
def createMos(mo_file,model_name,sweep_vars,plot_var,initial,increment,iterations,output_mos_path):
    first_half_str = first_half_skeleton.format(mo_file=mo_file,model_name=model_name,initial=initial,increment=increment,iterations=iterations)
    middle_str = ""
    for var in sweep_vars:
        sweep_str = xml_settings_skeleton.format(model_name=model_name,sweep_var=var)
        middle_str = middle_str + sweep_str
    ending_str = call_skeleton.format(model_name=model_name)
    final_str = first_half_str + middle_str + ending_str
    writeStrToFile(final_str,output_mos_path)



def writeStrToFile(str_,file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0


first_half_skeleton= \
"""// load the file
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
"""
xml_settings_skeleton= \
"""setInitXmlStartValue("{model_name}_init.xml", "{sweep_var}", String(value) , "{model_name}_init.xml");
  getErrorString();
"""
call_skeleton= \
"""// call the generated simulation code to produce a result file BouncingBall%i%_res.mat
  file_name_i := "{model_name}_" + String(i) + "_res.csv";
  //system("{model_name}.exe -r="+file_name_i);
  system("./{model_name} -r="+file_name_i);
  getErrorString();
  //plot(plot_var,fileName=file_name_i,externalWindow=true);
end for;
"""



if __name__ == "__main__":
    main()
