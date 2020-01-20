from __future__ import absolute_import
from aiida.orm import Str
from aiida.common import exceptions


class LogParser():
    """Parser class for parsing the log file."""
    def __init__(self, premod_calc):
        self.premod_calc = premod_calc

    def parse(self):
        """Parse log file of premod."""

        # Check if retrieved folder is present.
        try:
            output_folder = self.premod_calc.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER
        # Try to load the log file.
        try:
            with output_folder.open('PreModRun.log', 'r') as handle:
                result = self._parse_log(handle)
        except (OSError, IOError):
            return self.exit_codes.ERROR_READING_LOG_FILE
        if result is None:
            return self.exit_codes.ERROR_INVALID_LOG_OUTPUT

        return {'log': Str(result)}

    def _parse_log(self, file_handle):
        """Parse the content of the log file as a string."""
        return file_handle.readlines()
