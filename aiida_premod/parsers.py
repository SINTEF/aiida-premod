# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_premod.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import

from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory


class ParmameterParser():
    """
    Parse the input parameters for premod.
    """
    def __init__(self, data):
        """Initialize with a given AiiDA Dict instance."""
        if isinstance(data, get_data_class('dict')):
            self.data = data
        else:
            self._logger.warning(
                'Please supply an AiiDA Dict datatype for `data`.')
            self.data = None

    def write(dst):
        """Write the parameter file for premod at dst."""
        with open(dst, 'w') as handler:
            handler.write('MODE_SIM=' + self.data.ModeSim + '\n')
            handler.write('MODE_ENTITY=' + self.data.ModeEntity + '\n')
            handler.write('MODE_SD=' + self.data.ModeSD + '\n')
            handler.write('FILE_OUT_PPT=' + self.data.FILE_OUT_PPT + '\n')
            handler.write('OUTPUT_TIMES=' + str(len(self.data.OUTPUT_TIMES)) +
                          '\n')
            # Loop over the output times
            for time in self.data.OUTPUT_TIMES:
                handler.write(str(time) + ' ')
                handler.write('\n')
                handler.write('!' + '\n')
                handler.write('MODE_IO=' + self.data.ModeIO + '\n')
                handler.write('FILE_SOLVER=' + self.data.FILE_SOLVER + '\n')
                handler.write('FILE_ALLOY=' + self.data.FILE_ALLOY + '\n')
                handler.write('FILE_PROCESS=' + self.data.FILE_PROCESS + '\n')
                handler.write('FILE_PHASES=' + self.data.FILE_PHASES + '\n')
                handler.write('FILE_PPTLIB=' + self.data.FILE_PPTLIB + '\n')
                handler.write('FILE_PPTSIM=' + self.data.FILE_PPTSIM + '\n')

        return


class SummaryParser():
    """Parse summary file of premod."""
    def parse():
        """Try to load the summary file."""
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER
        try:
            with output_folder.open(
                    self.node.get_option('PremodRun/PremodRun_summary.txt'),
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


class PreModParser(Parser):
    """
    Parser class for parsing output of calculation.
    """
    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a PreModCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        from aiida.common import exceptions
        super(PreModParser, self).__init__(node)
        if not issubclass(node.process_class, PreModCalculation):
            raise exceptions.ParsingError("Can only parse PreModCalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        from aiida.orm import SinglefileData

        output_filename = self.node.get_option('output_filename')

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = ['PremodRun', 'PremodRun.log']
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error("Found files '{}', expected to find '{}'".format(
                files_retrieved, files_expected))
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES
        summary_parser = SummaryParser()
        summary_parser.parse()

        return ExitCode(0)
