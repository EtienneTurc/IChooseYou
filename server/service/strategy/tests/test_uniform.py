import pytest

from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.service.strategy.uniform import UniformStrategy
from server.tests.test_fixture import *  # noqa: F401, F403

channel_id = "42"
team_id = "1337"
user_id_inactive = "1233"
user_id_active = "1234"
current_user_id = "1234"


@pytest.mark.parametrize(
    "pick_list, weight_list, expected_item",
    [
        (["1", "2"], [1 / 2, 1 / 2], "1"),
    ],
)
def test_uniform_select_one_from_pick_list(
    pick_list, weight_list, expected_item, set_seed
):
    strategy = UniformStrategy(pick_list=pick_list, weight_list=weight_list)
    assert strategy.select_one_from_pick_list() == expected_item


@pytest.mark.parametrize(
    "pick_list, weight_list, number_of_items_to_select, expected_items",
    [
        (["1", "2"], [1 / 2, 1 / 2], 1, ["1"]),
        (["1", "2"], [1 / 2, 1 / 2], 2, ["1", "2"]),
        (["1", "2", "3"], [1 / 3, 1 / 3, 1 / 3], 2, ["1", "3"]),
        (["1", "2", "3"], [1 / 3, 1 / 3, 1 / 3], 5, ["1", "3", "2", "1", "2"]),
    ],
)
def test_uniform_select_from_pick_list(
    pick_list,
    weight_list,
    number_of_items_to_select,
    expected_items,
    set_seed,
):
    strategy = UniformStrategy(pick_list=pick_list, weight_list=weight_list)
    assert (
        strategy.select_from_pick_list(
            number_of_items_to_select=number_of_items_to_select
        )
        == expected_items
    )


@pytest.mark.parametrize(
    "pick_list, weight_list, number_of_items_to_select, only_active_users, self_exclude, expected_items",  # noqa E501
    [
        (["1", "2"], [1 / 2, 1 / 2], 1, False, False, ["1"]),
        (["1", "2"], [1 / 2, 1 / 2], 2, False, False, ["1", "2"]),
        (["1", "2", "3"], [1 / 3, 1 / 3, 1 / 3], 2, False, False, ["1", "3"]),
        (
            ["1", "2", "3"],
            [1 / 3, 1 / 3, 1 / 3],
            5,
            False,
            False,
            ["1", "3", "2", "1", "2"],
        ),
        (
            [
                f"<@{user_id_inactive}>",
                f"<@{user_id_active}>",
                f"<@{user_id_inactive}>",
            ],
            [1 / 3, 1 / 3, 1 / 3],
            2,
            True,
            False,
            [f"<@{user_id_active}>", f"<@{user_id_active}>"],
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1 / 2, 1 / 2],
            2,
            False,
            True,
            [f"<@{user_id_inactive}>", f"<@{user_id_inactive}>"],
        ),
    ],
)
def test_uniform_select(
    pick_list: list[str],
    weight_list: list[float],
    number_of_items_to_select: int,
    only_active_users: bool,
    self_exclude: bool,
    expected_items,
    set_seed,
):
    strategy = UniformStrategy(pick_list=pick_list, weight_list=weight_list)
    assert (
        strategy.select(
            number_of_items_to_select=number_of_items_to_select,
            self_exclude=self_exclude,
            user_id=current_user_id,
            only_active_users=only_active_users,
            team_id=team_id,
        )
        == expected_items
    )


@pytest.mark.parametrize(
    "pick_list, weight_list, self_exclude, only_active_users, error_message",
    [
        (
            [f"<@{current_user_id}>"],
            [1],
            True,
            False,
            "Pick list contains only the user using the command.",
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_inactive}>"],
            [1, 0],
            False,
            True,
            "All users in the pick list are inactive.",
        ),
        (
            [f"<@{current_user_id}>", f"<@{user_id_inactive}>"],
            [1, 0],
            True,
            True,
            "All users in the pick list are inactive.",
        ),
    ],
)
def test_uniform_select_errors(
    pick_list, weight_list, self_exclude, only_active_users, error_message
):
    strategy = UniformStrategy(pick_list=pick_list, weight_list=weight_list)
    with pytest.raises(MissingElementError, match=error_message):
        strategy.select(
            number_of_items_to_select=1,
            self_exclude=self_exclude,
            user_id=current_user_id,
            only_active_users=only_active_users,
            team_id=team_id,
        )
