#Std
import tempfile #para crear el tempdir

# Auxs for testing (create temp dir, create tmp file, etc)
def createTempFromContent(file_content,test_case):
    new_temp_f = tempfile.NamedTemporaryFile()
    new_temp_f.write(file_content)
    new_temp_f.seek(0)
    test_case._temp_files.append(new_temp_f)
    return new_temp_f.name
def outputDirPath(test_case):
    return test_case._temp_dir
