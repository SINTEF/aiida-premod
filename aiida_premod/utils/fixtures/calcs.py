"""
Fixtures for the VASP calculations.

-----------------------------------
Here we set up different pytest fixtures that are used to represent various VASP
calculations on which one can for instance test parsing etc.
"""
# pylint: disable=unused-import,unused-argument,redefined-outer-name
import pytest

from aiida.engine.utils import instantiate_process
from aiida.orm import Code
from aiida.common.extendeddicts import AttributeDict
from aiida.manage.manager import get_manager

from aiida_premod.utils.fixtures.computers import localhost

@pytest.fixture()
def calc_with_retrieved(localhost):
    """A rigged CalcJobNode for testing the parser and that the calculation retrieve what is expected."""
    from aiida.common.links import LinkType
    from aiida.orm import CalcJobNode, FolderData, Computer, Dict

    def _inner(file_path, input_settings=None):
        # Create a test computer
        computer = localhost

        process_type = 'aiida.calculations:{}'.format('premod')

        node = CalcJobNode(computer=computer, process_type=process_type)
        node.set_option('resources', {'num_machines': 1, 'num_mpiprocs_per_machine': 1})
        node.set_option('max_wallclock_seconds', 1800)

        if input_settings is None:
            input_settings = {}

        settings = Dict(dict=input_settings)
        node.add_incoming(settings, link_type=LinkType.INPUT_CALC, link_label='settings')
        settings.store()
        node.store()

        # Create a `FolderData` that will represent the `retrieved` folder. Store the files in
        # the file_path on the retrieved node.
        retrieved = FolderData()
        retrieved.put_object_from_tree(file_path)
        retrieved.add_incoming(node, link_type=LinkType.CREATE, link_label='retrieved')
        retrieved.store()

        return node

    return _inner
