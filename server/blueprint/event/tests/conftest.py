import pytest

from server.orm.command import Command
from server.service.strategy.enum import Strategy

TEST_COMMAND_NAME = "test_command_name"
TEST_COMMAND_PICK_LIST = ["first element", "second element", "third one"]
TEST_WEIGHT_LIST = [1 / 3, 1 / 3, 1 / 3]
TEST_STRATEGY = Strategy.uniform.name
TEST_COMMAND_LABEL = "label of the command"
TEST_COMMAND_CHANNEL_ID = "1234"
TEST_COMMAND_CREATED_BY = "1234"


@pytest.fixture()
def test_command():
    Command.create(
        name=TEST_COMMAND_NAME,
        channel_id=TEST_COMMAND_CHANNEL_ID,
        label=TEST_COMMAND_LABEL,
        pick_list=TEST_COMMAND_PICK_LIST,
        weight_list=TEST_WEIGHT_LIST,
        strategy=TEST_STRATEGY,
        self_exclude=False,
        only_active_users=False,
        created_by_user_id=TEST_COMMAND_CREATED_BY,
    )
