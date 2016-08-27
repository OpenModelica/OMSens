import os
import inspect
from datetime import datetime
import subprocess
import re #regex
import logging
logger = logging.getLogger("--Files aux funcs--") #un logger especifico para este modulo

# Functions to get current directory, create folder, create "tmp" folder to dump results, etc
def parentDir(dir_):
    return os.path.dirname(dir_)
def makeOutputPath(folder_name="modelica_output"):
    dest_path = destPath(folder_name)
    timestamp_dir = makeDirFromCurrentTimestamp(dest_path)
    return timestamp_dir

def makeDirFromCurrentTimestamp(dest_path):
    logger.debug("Making timestamp dir")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dateAndTime = datetime.now()
    new_folder_path = os.path.join(dest_path,dateAndTime.strftime('%Y-%m-%d/%H_%M_%S'))
    os.makedirs(new_folder_path)
    return new_folder_path
def destPath(folder_name):
    tmp_path = tmpPath()
    return os.path.join(tmp_path,folder_name)
def tmpPath():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = parentDir(currentdir)
    return os.path.join(parentdir,"tmp")
    # return os.path.join(currentdir,"tmp")

# Functions to modify filesystem:
def writeStrToFile(str_,file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0

def callCMDStringInPath(command,path):
    process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True,cwd=path)
    output = process.communicate()[0]
    return output

def removeFilesWithRegexAndPath(regex,folder_path):
    for x in os.listdir(folder_path):
        if re.match(regex, x):
            os.remove(os.path.join(folder_path,x))
