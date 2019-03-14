import shutil
import inspect
import logging
import os
import re  # regex
import subprocess
from datetime import datetime

logger = logging.getLogger("--Files aux funcs--")  # un logger especifico para este modulo


# Functions to get current directory, create folder, create "tmp" folder to dump results, etc

def parentDir(dir_):
    return os.path.dirname(dir_)


def makeOutputPath(folder_name="modelica_output"):
    dest_path = destPath(folder_name)
    timestamp_dir = makeDirFromCurrentTimestamp(dest_path)
    return timestamp_dir


def makeFolderWithPath(dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

def makeDirFromCurrentTimestamp(dest_path):
    logger.debug("Making timestamp dir")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dateAndTime = datetime.now()
    date = dateAndTime.strftime('%Y-%m-%d')
    time = dateAndTime.strftime('%H_%M_%S')
    new_folder_path = os.path.join(dest_path, date, time)
    os.makedirs(new_folder_path)
    return new_folder_path


def destPath(folder_name):
    tmp_path = tmpPath()
    return os.path.join(tmp_path, folder_name)


def projectRoot():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    project_root = parentDir(currentdir)
    return project_root

def tmpPath():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = parentDir(currentdir)
    return os.path.join(parentdir, "tmp")
    # return os.path.join(currentdir,"tmp")

def moFilePathFromJSONMoPath(json_mo_path):
    # Check if it's absolute path or relative path and act accordingly
    is_abs_path = os.path.isabs(json_mo_path)
    if is_abs_path:
        # If it's already an absolute path, there's nothing to do
        mo_file_path = json_mo_path
    else:
        # If it's a relative path, make it a relative path from the project root
        project_root_path = projectRoot()
        relative_to_project_root_path = os.path.join(project_root_path, json_mo_path)
        mo_file_path = os.path.abspath(relative_to_project_root_path)
    return mo_file_path


# Functions to modify filesystem:
def writeStrToFile(str_, file_path):
    with open(file_path, 'w') as outputFile:
        outputFile.write(str_)
    return 0


def callCMDStringInPath(command, path):
    # shell=True
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=path)
    # shell=False
    # # Make list of strings splitting by whitespaces
    # args = command.split(" ")
    # # Remove invalid args
    # args_cleaned = [x for x in args if x != ""]
    # process = subprocess.Popen(args_cleaned, stdout=subprocess.PIPE, shell=False, cwd=path)
    output = process.communicate()[0]
    return output


def removeFilesWithRegexAndPath(regex, folder_path):
    for x in os.listdir(folder_path):
        if re.match(regex, x):
            file_path = os.path.join(folder_path, x)
            if os.path.isfile(file_path):
                # If it's a file, call file deleter
                os.remove(file_path)
            elif os.path.isdir(file_path):
                # If it's a folder, call folder deleter
                shutil.rmtree(file_path)
            else:
                error_msg ="The file in path {0} to delete is neither a file or a folder".format(x)
                raise Exception(error_msg)


def readStrFromFile(file_path):
    with open(file_path, 'r') as myfile:
        data = myfile.read()
    return data
