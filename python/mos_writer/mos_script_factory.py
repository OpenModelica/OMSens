import inspect
from abc import ABC
# Mine:
import mos_writer.sweeping_mos_writer


# Abstract class that implements most of the functionaltity.
# The only responsibility of the subclasses is to set if uniparam or multiparam mos_writer
class MosScriptFactory(ABC):
    # Init
    def __init__(self, *args, **kwargs):
        self._settings_dict = kwargs.pop("settings_dict")

    def requiredSettings(self):
        required, optional = self.allSeteableSettings()
        return required

    def allSeteableSettings(self):
        # Returns the mandatory and the optional parameters
        argsspecmsf = inspect.getargspec(self._sweeping_mos_writer.createMos)
        if argsspecmsf.defaults:
            # If there are args with default values
            mandatory = argsspecmsf.args[0:len(argsspecmsf.args) - len(argsspecmsf.defaults)]
            optional = argsspecmsf.args[-len(argsspecmsf.defaults):]
        else:
            mandatory = argsspecmsf.args
            optional = []
        # Remove "self" from mandatory args (if any)
        mandatory = [x for x in mandatory if x != "self"]
        return mandatory, optional

    def setSetting(self, setting, value):
        self._settings_dict[setting] = value

    def initializedSettings(self):
        return self._settings_dict.copy()

    def missingSettings(self):
        missing_settings = []
        for k in self.requiredSettings():
            if not (k in self._settings_dict):
                missing_settings.append(k)
        return missing_settings

    def createMosScript(self):
        missing_settings = self.missingSettings()
        assert len(missing_settings) == 0, "You're missing settings:" + str(missing_settings)
        createMos_kwargs = self._settings_dict
        self._sweeping_mos_writer.createMos(**createMos_kwargs)


class UniparamMosScriptFactory(MosScriptFactory):
    # Init
    def __init__(self, *args, **kwargs):
        # Call superclass init with kwargs
        super(UniparamMosScriptFactory, self).__init__(*args, **kwargs)
        # Set the info for this subclass (if uniparam or multiparam factory)
        self._sweeping_mos_writer = mos_writer.sweeping_mos_writer.UniparamSweepingMosWriter()


class MultiparamMosScriptFactory(MosScriptFactory):
    # Init
    def __init__(self, *args, **kwargs):
        # Call superclass init with kwargs
        super(MultiparamMosScriptFactory, self).__init__(*args, **kwargs)
        # Set the info for this subclass (if uniparam or multiparam factory)
        self._sweeping_mos_writer = mos_writer.sweeping_mos_writer.MultiparamSweepingMosWriter()
