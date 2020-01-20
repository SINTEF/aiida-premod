"""
Fixtures for the premod calculations.

-----------------------------------
Here we set up different pytest fixtures that are used to represent various premod
calculations on which one can for instance test parsing etc.
"""
# pylint: disable=unused-import,unused-argument,redefined-outer-name
from __future__ import absolute_import
import pytest

# houses aiida_local_code_factory among others
pytest_plugins = ['aiida.manage.tests.pytest_fixtures']


@pytest.fixture(scope='function')
def premod_code(aiida_local_code_factory):
    """Get the premod code.
    """
    premod_code = aiida_local_code_factory(executable='premod',
                                           entry_point='premod')
    return premod_code
