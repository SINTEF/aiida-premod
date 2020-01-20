# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_premod.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import

from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

from aiida_premod.parsers.file_parsers.summary import SummaryParser
from aiida_premod.parsers.file_parsers.micro import MicroParser
from aiida_premod.parsers.file_parsers.log import LogParser


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
        super(PreModParser, self).__init__(node)
        if not issubclass(node.process_class, CalculationFactory('premod')):
            raise exceptions.ParsingError("Can only parse PreModCalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        # Check if retrieved folder is present
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDE

        # Check that folder content is as expected
        files_retrieved = output_folder.list_object_names()
        files_expected = ['PreModRun', 'PreModRun.log']
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error("Found files '{}', expected to find '{}'".format(
                files_retrieved, files_expected))
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES
        summary_parser = SummaryParser(self)
        summary = summary_parser.parse()
        self.out('summary', summary['summary'])
        log_parser = LogParser(self)
        log = log_parser.parse()
        self.out('log', log['log'])
        micro_parser = MicroParser(self)
        micro = micro_parser.parse()
        self.out('micro', micro['micro'])

        return ExitCode(0)
