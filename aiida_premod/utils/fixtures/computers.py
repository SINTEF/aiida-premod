import pytest

from aiida.orm import Computer
from aiida.common.exceptions import NotExistent
from aiida_premod.utils.fixtures.environment import fresh_aiida_env

@pytest.fixture(scope='session')
def localhost_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('localhost_work')

@pytest.fixture
def localhost(fresh_aiida_env, localhost_dir):
    """Fixture for a local computer called localhost."""
    try:
        computer = Computer.objects.get(name='localhost')
    except NotExistent:
        computer = Computer(name='localhost',
                            hostname='localhost',
                            transport_type='local',
                            scheduler_type='direct',
                            workdir=localhost_dir.strpath).store()
    return computer
