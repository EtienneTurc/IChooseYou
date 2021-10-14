import pytest

from server.orm.command import Command
from server.service.strategy.enum import Strategy
from server.tests.test_app import *  # noqa: F401, F403

default_command = {
    "name": "basic_command",
    "channel_id": "1234",
    "label": "basic command label",
    "description": "basic command description",
    "pick_list": ["1", "2", "3"],
    "self_exclude": False,
    "only_active_users": False,
    "weight_list": [1 / 3, 1 / 3, 1 / 3],
    "strategy": Strategy.uniform.name,
    "created_by_user_id": "1",
}


def create_and_return_command(**kwargs):
    Command.create(**kwargs)
    return Command.find_one_by_name_and_chanel(kwargs["name"], kwargs["channel_id"])


@pytest.fixture
def basic_command(client):
    command = create_and_return_command(**default_command)
    yield command
    Command.delete_command(command)


@pytest.fixture
def command_for_self_exclude(client):
    input = {
        **default_command,
        "pick_list": ["<@1234|name>", "2"],
        "weight_list": [1 / 2, 1 / 2],
        "self_exclude": True,
    }
    command = create_and_return_command(**input)
    yield command
    Command.delete_command(command)


@pytest.fixture
def command_for_self_exclude_error(client):
    input = {
        **default_command,
        "pick_list": ["<@1234|name>"],
        "weight_list": [1],
        "self_exclude": True,
    }
    command = create_and_return_command(**input)
    yield command
    Command.delete_command(command)


@pytest.fixture
def command_for_active_users(client):
    input = {
        **default_command,
        "pick_list": ["<@1234|name>"],
        "weight_list": [1],
        "only_active_users": True,
    }
    command = create_and_return_command(**input)
    yield command
    Command.delete_command(command)


@pytest.fixture
def command_with_no_active_users(client):
    input = {
        **default_command,
        "pick_list": ["<@4321|name>"],
        "weight_list": [1],
        "only_active_users": True,
    }
    command = create_and_return_command(**input)
    yield command
    Command.delete_command(command)
