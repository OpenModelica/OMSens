#Std
import tempfile #para crear el tempdir

# Auxs for testing (create temp dir, create tmp file, etc)
def createTempFromStrAndAddToTestCase(file_content,test_case,suffix=""):
    new_temp_f = createTempFromStr(file_content,suffix)
    test_case._temp_files.append(new_temp_f)
    return new_temp_f.name
def createTempFromStr(file_content,suffix):
    new_temp_f = tempfile.NamedTemporaryFile(suffix=suffix)
    new_temp_f.write(file_content)
    new_temp_f.seek(0)
    return new_temp_f
def outputDirPath(test_case):
    return test_case._temp_dir
