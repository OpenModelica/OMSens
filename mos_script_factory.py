import inspect
#Mine:
import sweeping_mos_writer
class MosScriptFactory():
    #Init
    def __init__(self,settings_dict):
        self._settings_dict = settings_dict
    def requiredSettings(self):
        required,optional = self.allSeteableSettings()
        return required
    def allSeteableSettings(self):
        #Returns the mandatory and the optional parameters
        argsspecmsf = inspect.getargspec(sweeping_mos_writer.createMos)
        if argsspecmsf.defaults:
            #If there are args with default values
            mandatory = argsspecmsf.args[0:len(argsspecmsf.args)-len(argsspecmsf.defaults)]
            optional = argsspecmsf.args[-len(argsspecmsf.defaults):]
        else:
            mandatory = argsspecmsf.args
            optional = []
        return mandatory,optional
    def setSetting(self,setting,value):
        self._settings_dict[setting] = value
    def initializedSettings(self):
        return self._settings_dict.copy()
    def missingSettings(self):
        missing_settings = []
        for k in self.requiredSettings():
            if not (k in self._settings_dict):
                missing_settings.append(k)
        return missing_settings

    def writeToFile(self):
        missing_settings = self.missingSettings()
        assert len(missing_settings)==0 , "You're missing settings:"+ str(missing_settings)
        sweeping_mos_writer.createMos(**self._settings_dict)
