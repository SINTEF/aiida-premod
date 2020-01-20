""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import os

from aiida.orm import Code
from aiida_premod import tests
from aiida_premod.utils.fixtures.calcs import premod_code
from aiida_premod.utils.fixtures.computers import localhost, localhost_dir
from aiida_premod.utils.fixtures.environment import fresh_aiida_env

def test_process(premod_code):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run

    # Name of calculation
    name = 'mypremodcalc'

    # Set input parameters
    parameters = DataFactory('dict')
    parameters.MODE_SIM='PPT'
    parameters.MODE_ENTITY='SD'
    parameters.MODE_SD='EULERIAN'
    parameters.FILE_OUT_PPT=name+'.out'
    parameters.OUTPUT_TIMES=[1800.00, 3600.00, 14400.00, 61200.00, 277200.00]
    parameters.MODE_IO='TXT'
    parameters.FILE_SOLVER='solver.txt'
    parameters.FILE_ALLOY='alloy.txt'
    parameters.FILE_PROCESS='temperature.txt'
    parameters.FILE_PHASES='libphases.txt'
    parameters.FILE_PPTLIB='models.txt'
    parameters.FILE_PPTSIM='libmodel.txt'
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
        'parameters': parameters,
        'alloy': alloy,
        'solver': solver,
        'temperature': temperature,
        'models': models,
        'libphases': libphases,
        'libmodel': libmodel,
        'metadata': {
            'description': "Test job submission with the aiida_premod plugin",
            'label': name,
        },
    }
    print(inputs['parameters'])
    result = run(CalculationFactory('premod'), **inputs)
