import pytest

from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.service.strategy.smooth import SmoothStrategy
from server.tests.test_fixture import *  # noqa: F401, F403

default_pick_list = ["1", "2", "3", "4"]
channel_id = "42"
team_id = "1337"
user_id_inactive = "1233"
user_id_active = "1234"
current_user_id = "1234"


@pytest.mark.parametrize(
    "initial_weight_list, indices_selected, expected_weight_list",
    [
        ([1], [0], [1]),
        ([1, 0], [0], [1, 0]),
        ([1 / 2, 1 / 2], [0], [1 / 3, 2 / 3]),
        ([1 / 3, 2 / 3], [0], [3 / 11, 8 / 11]),
        ([1 / 3, 2 / 3], [1], [4 / 7, 3 / 7]),
        ([1 / 4, 1 / 4, 1 / 4, 1 / 4], [0], [1 / 13, 4 / 13, 4 / 13, 4 / 13]),
        ([1 / 3, 2 / 3], [0, 1], [1 / 2, 1 / 2]),
        ([1 / 3, 1 / 3, 1 / 3], [0, 1], [3 / 14, 3 / 14, 8 / 14]),
    ],
)
def test_smooth_update(initial_weight_list, indices_selected, expected_weight_list):
    result = SmoothStrategy(
        pick_list=default_pick_list[: len(initial_weight_list)],
        weight_list=initial_weight_list,
    ).update(indices_selected=indices_selected)
    assert [round(el, 6) for el in result] == [
        round(el, 6) for el in expected_weight_list
    ]


@pytest.mark.parametrize(
    "pick_list, weight_list, expected_item",
    [
        (["1", "2"], [1 / 2, 1 / 2], "1"),
    ],
)
def test_smooth_select_one_from_pick_list(
    pick_list, weight_list, expected_item, set_seed
):
    strategy = SmoothStrategy(pick_list=pick_list, weight_list=weight_list)
    assert strategy.select_one_from_pick_list() == expected_item


@pytest.mark.parametrize(
    "pick_list, weight_list, number_of_items_to_select, expected_items",
    [
        (["1", "2"], [1 / 2, 1 / 2], 1, ["1"]),
        (["1", "2"], [1 / 2, 1 / 2], 2, ["1", "2"]),
        (["1", "2", "3"], [1 / 3, 1 / 3, 1 / 3], 2, ["1", "3"]),
        (["1", "2", "3"], [1 / 6, 2 / 6, 3 / 6], 5, ["1", "3", "2", "2", "3"]),
    ],
)
def test_smooth_select_from_pick_list(
    pick_list,
    weight_list,
    number_of_items_to_select,
    expected_items,
    set_seed,
):
    strategy = SmoothStrategy(pick_list=pick_list, weight_list=weight_list)
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
def test_smooth_select(
    pick_list: list[str],
    weight_list: list[float],
    number_of_items_to_select: int,
    only_active_users: bool,
    self_exclude: bool,
    expected_items,
    set_seed,
):
    strategy = SmoothStrategy(pick_list=pick_list, weight_list=weight_list)
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
def test_smooth_select_errors(
    pick_list, weight_list, self_exclude, only_active_users, error_message
):
    strategy = SmoothStrategy(pick_list=pick_list, weight_list=weight_list)
    with pytest.raises(MissingElementError, match=error_message):
        strategy.select(
            number_of_items_to_select=1,
            self_exclude=self_exclude,
            user_id=current_user_id,
            only_active_users=only_active_users,
            team_id=team_id,
        )
