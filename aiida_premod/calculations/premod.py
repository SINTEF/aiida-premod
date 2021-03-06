"""
Base calculations provided by aiida_premod.

Register calculations via the "aiida.base" entry point in setup.json.
"""
from __future__ import absolute_import

import six

from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData
from aiida.plugins import DataFactory

from aiida_premod.parsers.file_parsers.parameter import ParameterParser


class PreModCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the premod executable.

    This executable calculates the precipication...
    """
    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super(PreModCalculation, cls).define(spec)
        spec.input('metadata.options.resources', valid_type=dict, default={'num_machines': 1, 'num_mpiprocs_per_machine': 1})
        spec.input('metadata.options.parser_name', valid_type=six.string_types, default='premod')
        spec.input('metadata.options.withmpi', valid_type=bool, default=False)
        spec.input('parameters', valid_type=DataFactory('dict'), help='Parameters for premod')
        spec.input('alloy', valid_type=SinglefileData, help='Alloy description.')
        spec.input('solver', valid_type=SinglefileData, help='Second file to be compared.')
        spec.input('temperature', valid_type=SinglefileData, help='Second file to be compared.')
        spec.input('models', valid_type=SinglefileData, help='Second file to be compared.')
        spec.input('libphases', valid_type=SinglefileData, help='Second file to be compared.')
        spec.input('libmodel', valid_type=SinglefileData, help='Second file to be compared.')

        spec.output('log', valid_type=DataFactory('str'), help='The log generated by premod.')
        spec.output('summary', valid_type=DataFactory('str'), help='A summary of the results.')
        spec.output('micro', valid_type=DataFactory('array'), help='A history.')

        spec.exit_code(1000, 'ERROR_MISSING_INPUT_FILES', message='Expected input files was not supplied.')
        spec.exit_code(1001, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')
        spec.exit_code(1002, 'ERROR_NO_RETRIEVED_FOLDER', message='Retrieved folder does not exist.')
        spec.exit_code(1003, 'ERROR_INVALID_SUMMARY_OUTPUT', message='Parsing of the summary output file failed.')
        spec.exit_code(1004, 'ERROR_READING_SUMMARY_FILE', message='Failed to read the summary file.')

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """

        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.withmpi = self.inputs.metadata.options.withmpi
        codeinfo.cmdline_params = ['PreModRun.txt']

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = [
            (self.inputs.alloy.uuid, self.inputs.alloy.filename, self.inputs.alloy.filename),
            (self.inputs.solver.uuid, self.inputs.solver.filename, self.inputs.solver.filename),
            (self.inputs.temperature.uuid, self.inputs.temperature.filename, self.inputs.temperature.filename),
            (self.inputs.models.uuid, self.inputs.models.filename, self.inputs.models.filename),
            (self.inputs.libphases.uuid, self.inputs.libphases.filename, self.inputs.libphases.filename),
            (self.inputs.libmodel.uuid, self.inputs.libmodel.filename, self.inputs.libmodel.filename),
        ]
        calcinfo.retrieve_list = ['PreModRun','PreModRun.log']

        # write input file
        parameter_parser = ParameterParser(data=self.inputs.parameters)
        parameter_parser.write(folder.get_abs_path('PreModRun.txt'))

        return calcinfo
