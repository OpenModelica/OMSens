#This is the main script for configuring, running and plotting a OpenModelica Sweep
# 1) Set up run:
#    a) Get .mo
#    b) get initial configuration (standard config)
#    c) get new parameters (parameters that differ from the standard)
#    d) Choose between .mos script or OMPython:
#       A) .mos:
#          A.1) Create output folder (recycle "timestamp dir" from MML_Extra_Scripts)
#          A.2) Create .mos file in output folder from .mos skeleton that includes the following:
#               A.3.1) Build model: this will create a binary and a .xml file.
#                      A.3.1.Alternate.1) If the model doesn't include an initial configuration and no .xml
#                        file was created, create one yourself from 1.b).
#                      A.3.Alternate.2) If the .xml file has the initial configuration from 1.b), then just
#                        use it and don't do anything.
#               A.3.2) Set the new parameters from 1.c) to the .xml file and run it
#               A.3.3) repeat A.3.2) for all the sets of parameters.
#         A.3) Run the .mos file with command omc
#         A.4) Delete all the {model_name}* temporary files created by the build
#       B) Very similar to A) but "live" with process comunication using OMPYthon instead of
#          creating a .mos file
#   e) Plot using python or OMPlot:
#      A) Python:
#         A.1) Get all the csv files and the variables to plot for each experiment
#         A.2) Setup pyplot
#         A.3) Get the data for a .csv using np
#         A.4) plot using the variable to choose the column from the data, "variable_file" as label
#              and column "time" as x axis
#         A.5) repeat A.4) for all the variables
#         A.6) repeat A.3)-A.5) for all the csvs
#      B) OMPlot:
#        a) Read Adeel's new mail and find out how to plot multiple experiments from the same model
#           in the same plot
import os
from datetime import datetime
import inspect
# My imports
def currentDir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def parentDir(dir_):
    return os.path.dirname(dir_)


import logging #en reemplazo de los prints
logger = logging.getLogger("--Run and Plot OpenModelica--") #un logger especifico para este modulo

def main():
    output_path = makeOutputPath()

def makeOutputPath():
    dest_path = destPath()
    timestamp_dir = makeDirFromCurrentTimestamp(dest_path)

def makeDirFromCurrentTimestamp(dest_path):
    logger.debug("Making timestamp dir")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dateAndTime = datetime.now()
    new_folder_path = os.path.join(dest_path,dateAndTime.strftime('%Y-%m-%d/%H_%M_%S'))
    os.makedirs(new_folder_path)
    return new_folder_path
def destPath():
    tmp_path = tmpPath()
    return os.path.join(tmp_path,"csv_analysis")
def tmpPath():
    currentdir = currentDir()
    parentdir = parentDir(currentdir)
    # return os.path.join(parentdir,"tmp")
    return os.path.join(currentdir,"tmp")


if __name__ == "__main__":
    main()

