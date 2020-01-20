from aiida.common import exceptions

class SummaryParser():
    """Parser class for parsing the summary file."""
    def __init__(self, premod_calc):
        self.premod_calc = premod_calc

    """Parse summary file of premod."""
    def parse(self):
        # Check if retrieved folder is present
        try:
            output_folder = self.premod_calc.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDE

        """Try to load the summary file."""
        try:
            with output_folder.open(
                    self.premod_calc.node.get_option('PreModRun/PreModRun_summary.txt'),
                    'r') as handle:
                result = self._parse_summary(handle)
        except (OSError, IOError):
            return self.exit_codes.ERROR_READING_OUTPUT_FILE
        if result is None:
            return self.exit_codes.ERROR_INVALID_OUTPUT

        self.out('summary', Str(result))

    def _parse(file_handle):
        """Parse the content of the summary file as a string."""
        return file_handler.readline()
