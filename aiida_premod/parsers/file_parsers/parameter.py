from __future__ import absolute_import
from aiida.plugins import DataFactory
from aiida.common.extendeddicts import AttributeDict


class ParameterParser():
    """
    Parse the input parameters for premod.
    """
    def __init__(self, data):
        """Initialize with a given AiiDA Dict instance."""
        if isinstance(data, type(DataFactory('dict')(dict={}))):
            self.data = data
        else:
            self._logger.warning(
                'Please supply an AiiDA Dict datatype for `data`.')
            self.data = None

    def write(self, dst):
        """Write the parameter file for premod at dst."""
        with open(dst, 'w') as handler:
            data = AttributeDict(self.data.get_dict())
            handler.write('MODE_SIM=' + data.MODE_SIM + '\n')
            handler.write('MODE_ENTITY=' + data.MODE_ENTITY + '\n')
            handler.write('MODE_SD=' + data.MODE_SD + '\n')
            handler.write('FILE_OUT_PPT=' + data.FILE_OUT_PPT + '\n')
            handler.write('OUTPUT_TIMES=' + str(len(data.OUTPUT_TIMES)) + '\n')
            # Loop over the output times
            for time in data.OUTPUT_TIMES:
                handler.write(str(time) + ' ')
            handler.write('\n')
            #handler.write('!' + '\n')
            handler.write('MODE_IO=' + data.MODE_IO + '\n')
            handler.write('FILE_SOLVER=' + data.FILE_SOLVER + '\n')
            handler.write('FILE_ALLOY=' + data.FILE_ALLOY + '\n')
            handler.write('FILE_PROCESS=' + data.FILE_PROCESS + '\n')
            handler.write('FILE_PHASES=' + data.FILE_PHASES + '\n')
            handler.write('FILE_PPTLIB=' + data.FILE_PPTLIB + '\n')
            handler.write('FILE_PPTSIM=' + data.FILE_PPTSIM + '\n')
