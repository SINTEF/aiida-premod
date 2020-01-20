from __future__ import absolute_import
from os import path
import numpy as np

from aiida.common import exceptions
from aiida.plugins import DataFactory


class MicroParser():
    """Parser class for parsing the micro files."""
    def __init__(self, premod_calc):
        self.premod_calc = premod_calc

    def parse(self):
        """Parse micro files of premod."""

        # Check if retrieved folder is present.
        try:
            output_folder = self.premod_calc.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER
        # Try to load the micro files.
        files_in_folder = output_folder.list_object_names('PreModRun')
        micro_files = [
            path.join('PreModRun', filename) for filename in files_in_folder
            if 'PreModRun_Micro' in filename
        ]
        index = 0
        micro_array = DataFactory('array')()
        for filename in micro_files:
            try:
                with output_folder.open(filename, 'r') as handle:
                    result = self._parse_micro(handle)
            except (OSError, IOError):
                return self.exit_code.ERROR_READING_MICRO_FILE
            if result is None:
                return self.exit_code.ERROR_INVALID_MICRO_OUTPUT
            micro_array.set_array('step_' + str(index), result)
            index = index + 1

        return {'micro': micro_array}

    def _parse_micro(self, file_handle):
        """Parse the content of the micro file as a string."""
        data = file_handle.readlines()
        micro_data_start_index = [
            index for index, item in enumerate(data) if "DomainID" in item
        ][0] + 1
        micro_data = data[micro_data_start_index:]
        micro_data_prepped = []
        for line in micro_data:
            line_prepped = [float(item) for item in line.strip().split()[1:4]]
            micro_data_prepped.append(line_prepped)

        return np.array(micro_data_prepped)
