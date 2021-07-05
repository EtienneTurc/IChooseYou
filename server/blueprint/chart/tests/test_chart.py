from server.blueprint.chart.service import create_heat_map
from server.blueprint.event.tests.conftest import *  # noqa: F401, F403
from server.blueprint.event.tests.conftest import (TEST_COMMAND_CHANNEL_ID,
                                                   TEST_COMMAND_NAME)
from server.tests.test_app import *  # noqa: F401, F403
from server.tests.test_fixture import *  # noqa: F401, F403


def test_create_heat_map(client, test_command, set_seed):  # noqa F811
    _, mimetype = create_heat_map(TEST_COMMAND_NAME, TEST_COMMAND_CHANNEL_ID)
    assert True
    assert mimetype == "image/png"
