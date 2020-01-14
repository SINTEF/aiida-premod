# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function
import os
from aiida.orm import Code
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run

# get code
code_string = 'premod@localhost'
code = Code.get_from_string(code_string)

# Prepare input parameters
#DiffParameters = DataFactory('premod')
#parameters = DiffParameters({'ignore-case': True})

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
    'code': code,
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

# Note: in order to submit your calculation to the AiiDA daemon, do:
# from aiida.engine import submit
# future = submit(CalculationFactory('premod'), **inputs)
result = run(CalculationFactory('premod'), **inputs)

computed_diff = result['premod'].get_content()
print("Computed diff between files: \n{}".format(computed_diff))
