""" Tests for calculations

"""
# pylint: disable=unused-import
from __future__ import print_function
from __future__ import absolute_import

import os

from aiida.common.extendeddicts import AttributeDict
from aiida_premod import tests
from aiida_premod.utils.fixtures.codes import premod_code  # noqa: F401


def test_process(premod_code):  # noqa: F811
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run

    # Set input parameters
    parameters = AttributeDict()
    parameters.MODE_SIM = 'PPT'
    parameters.MODE_ENTITY = 'SD'
    parameters.MODE_SD = 'EULERIAN'
    parameters.FILE_OUT_PPT = 'PreModRun.out'
    parameters.OUTPUT_TIMES = [1800.00, 3600.00, 14400.00, 61200.00, 277200.00]
    parameters.MODE_IO = 'TXT'
    parameters.FILE_SOLVER = 'solver.txt'
    parameters.FILE_ALLOY = 'alloy.txt'
    parameters.FILE_PROCESS = 'temperature.txt'
    parameters.FILE_PHASES = 'libphases.txt'
    parameters.FILE_PPTLIB = 'models.txt'
    parameters.FILE_PPTSIM = 'libmodel.txt'
    #paramters.ALPHA_PHASE=1

    # Fetch the single file AiiDA data structure
    SinglefileData = DataFactory('singlefile')

    alloy = SinglefileData(
        file=os.path.join(tests.TEST_DIR, 'input_files', 'alloy.txt'))
    solver = SinglefileData(
        file=os.path.join(tests.TEST_DIR, 'input_files', 'solver.txt'))
    temperature = SinglefileData(
        file=os.path.join(tests.TEST_DIR, 'input_files', 'temperature.txt'))
    models = SinglefileData(
        file=os.path.join(tests.TEST_DIR, 'input_files', 'models.txt'))
    libphases = SinglefileData(
        file=os.path.join(tests.TEST_DIR, 'input_files', 'libphases.txt'))
    libmodel = SinglefileData(
        file=os.path.join(tests.TEST_DIR, 'input_files', 'libmodel.txt'))

    # set up calculation
    inputs = {
        'code': premod_code,
        'parameters': DataFactory('dict')(dict=parameters),
        'alloy': alloy,
        'solver': solver,
        'temperature': temperature,
        'models': models,
        'libphases': libphases,
        'libmodel': libmodel,
        'metadata': {
            'description': "Test job submission with the aiida_premod plugin",
            'label': 'A calculation test',
        },
    }
    result = run(CalculationFactory('premod'), **inputs)
    # Add more sensible tests
    assert 'retrieved' in result
    assert 'log' in result
    assert 'micro' in result
    assert 'summary' in result
    assert 'Phase' in result['summary'].value
    assert 'info' in result['log'].value
