import random

import pytest

from server.service.selection.selection import (
    select_from_pick_list,
    select_one_from_pick_list,
)
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.service.strategy.enum import Strategy
from server.tests.test_fixture import *  # noqa: F401, F403

random.seed(10)

channel_id = "42"
team_id = "1337"
user_id_inactive = "1233"
user_id_active = "1234"


@pytest.mark.parametrize(
    "pick_list, weight_list, only_active_users, expected_item",
    [
        (
            ["1", "2"],
            [1 / 2, 1 / 2],
            False,
            ("1", ["1", "2"], [1 / 2, 1 / 2]),
        ),  # Deterministic because the seed is set
        (["1", "2"], [0, 1], False, ("2", ["1", "2"], [0, 1])),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1 / 2, 1 / 2],
            True,
            (f"<@{user_id_active}>", [f"<@{user_id_active}>"], [1]),
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1, 0],
            True,
            (f"<@{user_id_active}>", [f"<@{user_id_active}>"], [1]),
        ),
        (
            [user_id_inactive, f"<@{user_id_active}>"],
            [1, 0],
            True,
            (user_id_inactive, [user_id_inactive, f"<@{user_id_active}>"], [1, 0]),
        ),
        (
            [],
            [],
            False,
            (None, [], []),
        ),
        (
            [],
            [],
            True,
            (None, [], []),
        ),
    ],
)
def test_select_one_from_pick_list(
    pick_list, weight_list, only_active_users, expected_item, set_seed
):
    assert (
        select_one_from_pick_list(
            pick_list,
            weight_list,
            team_id=team_id,
            only_active_users=only_active_users,
        )
        == expected_item
    )


@pytest.mark.parametrize(
    "pick_list, weight_list, strategy_name, number_of_items_to_select, only_active_users, expected_items",  # noqa E501
    [
        (
            ["1", "2"],
            [1 / 2, 1 / 2],
            Strategy.uniform.name,
            1,
            False,
            ["1"],
        ),  # Deterministic because the seed is set
        (
            ["1", "2"],
            [0, 1],
            Strategy.round_robin.name,
            1,
            False,
            ["2"],
        ),
        (
            ["1", "2"],
            [1 / 2, 1 / 2],
            Strategy.uniform.name,
            2,
            False,
            ["1", "2"],
        ),
        (
            ["1", "2", "3"],
            [1 / 3, 1 / 3, 1 / 3],
            Strategy.uniform.name,
            2,
            False,
            ["1", "3"],
        ),
        (
            ["1", "2", "3"],
            [0, 1, 0],
            Strategy.round_robin.name,
            2,
            False,
            ["2", "3"],
        ),
        (
            ["1", "2", "3"],
            [0, 1, 0],
            Strategy.round_robin.name,
            4,
            False,
            ["2", "3", "1", "2"],
        ),
        (
            ["1", "2", "3"],
            [1 / 3, 1 / 3, 1 / 3],
            Strategy.uniform.name,
            5,
            False,
            ["1", "3", "2", "1", "2"],
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1 / 2, 1 / 2],
            Strategy.uniform.name,
            2,
            True,
            [f"<@{user_id_active}>", f"<@{user_id_active}>"],
        ),
        (
            [user_id_inactive, f"<@{user_id_active}>"],
            [1, 0],
            Strategy.round_robin.name,
            3,
            True,
            [user_id_inactive, f"<@{user_id_active}>", user_id_inactive],
        ),
    ],
)
def test_select_from_pick_list(
    pick_list,
    weight_list,
    strategy_name,
    number_of_items_to_select,
    only_active_users,
    expected_items,
    set_seed,
):
    assert (
        select_from_pick_list(
            initial_pick_list=pick_list,
            initial_weight_list=weight_list,
            strategy_name=strategy_name,
            number_of_items_to_select=number_of_items_to_select,
            team_id=team_id,
            only_active_users=only_active_users,
        )
        == expected_items
    )
