import random

import pytest

from server.service.selection.selection import select_from_pick_list
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.tests.test_fixture import *  # noqa: F401, F403

random.seed(10)

channel_id = "42"
team_id = "1337"
user_id_inactive = "1233"
user_id_active = "1234"


@pytest.mark.parametrize(
    "pick_list, weight_list, only_active_users, expected_element",
    [
        (
            ["1", "2"],
            [1 / 2, 1 / 2],
            False,
            "1",
        ),  # Deterministic because the seed is set
        (["1", "2"], [0, 1], False, "2"),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1 / 2, 1 / 2],
            True,
            f"<@{user_id_active}>",
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1, 0],
            True,
            f"<@{user_id_active}>",
        ),
        (
            [user_id_inactive, f"<@{user_id_active}>"],
            [1, 0],
            True,
            user_id_inactive,
        ),
        (
            [],
            [],
            False,
            None,
        ),
        (
            [],
            [],
            True,
            None,
        ),
    ],
)
def test_select_from_pick_list(
    pick_list, weight_list, only_active_users, expected_element, set_seed
):
    assert (
        select_from_pick_list(
            pick_list,
            weight_list,
            team_id=team_id,
            only_active_users=only_active_users,
        )
        == expected_element
    )
