import os
import inspect
from datetime import datetime
import logging
logger = logging.getLogger("--Files aux funcs--") #un logger especifico para este modulo

# Functions to get current directory, create folder, create "tmp" folder to dump results, etc
def currentDir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def parentDir(dir_):
    return os.path.dirname(dir_)
def makeOutputPath():
    dest_path = destPath()
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
def destPath():
    tmp_path = tmpPath()
    return os.path.join(tmp_path,"modelica_outputs")
def tmpPath():
    currentdir = currentDir()
    parentdir = parentDir(currentdir)
    # return os.path.join(parentdir,"tmp")
    return os.path.join(currentdir,"tmp")
