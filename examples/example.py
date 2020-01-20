# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function
import os
from aiida.orm import Code
from aiida.common.extendeddicts import AttributeDict
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run
from aiida import load_profile
load_profile()

from aiida_premod.tests import TEST_DIR  # pylint: disable=wrong-import-position

# get code
code_string = 'premod@localhost'
code = Code.get_from_string(code_string)

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

alloy = SinglefileData(file=os.path.join(TEST_DIR, 'input_files', 'alloy.txt'))
solver = SinglefileData(
    file=os.path.join(TEST_DIR, 'input_files', 'solver.txt'))
temperature = SinglefileData(
    file=os.path.join(TEST_DIR, 'input_files', 'temperature.txt'))
models = SinglefileData(
    file=os.path.join(TEST_DIR, 'input_files', 'models.txt'))
libphases = SinglefileData(
    file=os.path.join(TEST_DIR, 'input_files', 'libphases.txt'))
libmodel = SinglefileData(
    file=os.path.join(TEST_DIR, 'input_files', 'libmodel.txt'))

# set up calculation
inputs = {
    'code': code,
    'parameters': DataFactory('dict')(dict=parameters),
    'alloy': alloy,
    'solver': solver,
    'temperature': temperature,
    'models': models,
    'libphases': libphases,
    'libmodel': libmodel,
    'metadata': {
        'description': "Test job submission with the aiida_premod plugin",
        'label': 'This is a sample calculation'
    },
}

# Note: in order to submit your calculation to the AiiDA daemon, do:
# from aiida.engine import submit
# future = submit(CalculationFactory('premod'), **inputs)
result = run(CalculationFactory('premod'), **inputs)
