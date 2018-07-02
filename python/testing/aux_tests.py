# Std
import os
import tempfile  # para crear el tempdir


# Auxs for testing (create temp dir, create tmp file, etc)
def createTempFromStrIntoTestCaseTempFolder(file_content, test_case, temp_name):
    # create temp file in temp folder
    temp_folder_path = test_case._temp_dir
    temp_path = os.path.join(temp_folder_path, temp_name)
    with open(temp_path, "w") as outf:
        # outf.write(str(file_content,'utf-8'))
        outf.write(file_content)
    return temp_path


def createTempFromStrAndAddToTestCase(file_content, test_case, suffix=""):
    # Create standalone temp
    new_temp_f = createStandaoleTempFromStr(file_content, suffix)
    test_case._temp_files.append(new_temp_f)
    return new_temp_f.name


def createStandaoleTempFromStr(file_content, suffix):
    new_temp_f = tempfile.NamedTemporaryFile(suffix=suffix)
    new_temp_f.write(file_content)
    new_temp_f.seek(0)
    return new_temp_f


def outputDirPath(test_case):
    return test_case._temp_dir
