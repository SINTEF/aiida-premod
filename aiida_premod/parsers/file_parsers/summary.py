from __future__ import absolute_import
from aiida.orm import Str
from aiida.common import exceptions


class SummaryParser():
    """Parser class for parsing the summary file."""
    def __init__(self, premod_calc):
        self.premod_calc = premod_calc

    def parse(self):
        """Parse summary file of premod."""

        # Check if retrieved folder is present.
        try:
            output_folder = self.premod_calc.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER
        # Try to load the summary file.
        try:
            with output_folder.open('PreModRun/PreModRun_summary.txt',
                                    'r') as handle:
                result = self._parse_summary(handle)
        except (OSError, IOError):
            return self.exit_codes.ERROR_READING_SUMMARY_FILE
        if result is None:
            return self.exit_codes.ERROR_INVALID_SUMMARY_OUTPUT

        return {'summary': Str(result)}

    def _parse_summary(self, file_handle):
        """Parse the content of the summary file as a string."""
        return file_handle.readlines()
