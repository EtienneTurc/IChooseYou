import pytest

from server.service.error.type.missing_element_error import MissingElementError
from server.service.slack.tests.monkey_patch import *  # noqa: F401, F403
from server.service.strategy.round_robin import RoundRobinStrategy
from server.tests.test_fixture import *  # noqa: F401, F403

default_pick_list = ["1", "2", "3", "4"]


def test_round_robin_create_weight_list():
    assert RoundRobinStrategy.create_weight_list(3) == [1, 0, 0]


@pytest.mark.parametrize(
    "initial_weight_list, expected_weight_list",
    [
        ([1, 0, 0, 0], [0, 1, 0, 0]),
        ([0, 1, 0, 0], [0, 0, 1, 0]),
        ([0, 0, 1, 0], [0, 0, 0, 1]),
        ([0, 0, 0, 1], [1, 0, 0, 0]),
    ],
)
def test_round_robin_shift_selected_index(initial_weight_list, expected_weight_list):
    strategy = RoundRobinStrategy(
        pick_list=default_pick_list[: len(initial_weight_list)],
        weight_list=initial_weight_list,
    )
    strategy.shift_selected_index()
    assert strategy.weight_list == expected_weight_list


@pytest.mark.parametrize(
    "initial_weight_list, indices_selected, expected_pick_list, expected_weight_list",
    [
        ([1, 0, 0, 0], [0], ["1", "2", "3", "4"], [0, 1, 0, 0]),
        ([0, 1, 0, 0], [1], ["2", "3", "4", "1"], [0, 1, 0, 0]),
        ([0, 0, 1, 0], [2], ["3", "4", "1", "2"], [0, 1, 0, 0]),
        ([0, 0, 0, 1], [3], ["4", "1", "2", "3"], [0, 1, 0, 0]),
        ([0, 1, 0, 0], [1, 2], ["2", "3", "4", "1"], [0, 0, 1, 0]),
        ([0, 1, 0, 0], [1, 3], ["2", "4", "3", "1"], [0, 0, 1, 0]),
        ([0, 1, 0, 0], [1, 3], ["2", "4", "3", "1"], [0, 0, 1, 0]),
        ([0, 1, 0, 0], [1, 3, 0], ["2", "4", "1", "3"], [0, 0, 0, 1]),
        ([0, 1, 0, 0], [1, 2, 3, 0], ["2", "3", "4", "1"], [1, 0, 0, 0]),
    ],
)
def test_round_robin_update_weight_list(
    initial_weight_list, indices_selected, expected_pick_list, expected_weight_list
):
    strategy = RoundRobinStrategy(
        pick_list=default_pick_list[: len(initial_weight_list)],
        weight_list=initial_weight_list,
    )
    strategy.update(indices_selected=indices_selected)
    assert strategy.pick_list == expected_pick_list
    assert strategy.weight_list == expected_weight_list


@pytest.mark.parametrize(
    "items_to_add, weight_list, expected_weight_list",
    [
        (["c"], [1, 0], [1, 0, 0]),
        (["c", "d"], [1, 0], [1, 0, 0, 0]),
        (["c", "d"], [0, 1], [0, 1, 0, 0]),
    ],
)
def test_round_robin_add_items(items_to_add, weight_list, expected_weight_list):
    strategy = RoundRobinStrategy(
        pick_list=default_pick_list[: len(weight_list)], weight_list=weight_list
    )
    strategy.add_items(items_to_add)
    assert strategy.pick_list == default_pick_list[: len(weight_list)] + items_to_add
    assert strategy.weight_list == expected_weight_list


@pytest.mark.parametrize(
    "indices, weight_list, expected_weight_list",
    [
        ([1], [1, 0, 0, 0], [1, 0, 0]),
        ([1, 2, 3], [1, 0, 0, 0], [1]),
        ([0], [1, 0, 0, 0], [1, 0, 0]),
        ([1], [0, 1, 0, 0], [0, 1, 0]),
        ([1, 2], [0, 1, 0, 0], [0, 1]),
    ],
)
def test_round_robin_remove_item(indices, weight_list, expected_weight_list):
    strategy = RoundRobinStrategy(
        pick_list=default_pick_list[: len(weight_list)], weight_list=weight_list
    )
    strategy.remove_items(indices)
    assert strategy.weight_list == expected_weight_list

    # -------------------------------------------------------------------------
    # ----------------------------- SELECTION ---------------------------------
    # -------------------------------------------------------------------------


channel_id = "42"
team_id = "1337"
user_id_inactive = "1233"
user_id_active = "1234"
current_user_id = "1234"


@pytest.mark.parametrize(
    "pick_list, weight_list, expected_item",
    [
        (["1", "2"], [1, 0], "1"),
        (["1", "2"], [0, 1], "2"),
    ],
)
def test_round_robin_select_one_from_pick_list(
    pick_list, weight_list, expected_item, set_seed
):
    strategy = RoundRobinStrategy(pick_list=pick_list, weight_list=weight_list)
    assert strategy.select_one_from_pick_list() == expected_item


@pytest.mark.parametrize(
    "pick_list, weight_list, number_of_items_to_select, expected_items",
    [
        (["1", "2"], [0, 1], 1, ["2"]),
        (["1", "2", "3"], [0, 1, 0], 2, ["2", "3"]),
        (["1", "2", "3"], [0, 1, 0], 4, ["2", "3", "1", "2"]),
    ],
)
def test_round_robin_select_from_pick_list(
    pick_list,
    weight_list,
    number_of_items_to_select,
    expected_items,
    set_seed,
):
    strategy = RoundRobinStrategy(pick_list=pick_list, weight_list=weight_list)
    assert (
        strategy.select_from_pick_list(
            number_of_items_to_select=number_of_items_to_select
        )
        == expected_items
    )


@pytest.mark.parametrize(
    "pick_list, weight_list, number_of_items_to_select, only_active_users, self_exclude, expected_items",  # noqa E501
    [
        (
            ["1", "2"],
            [0, 1],
            1,
            False,
            False,
            ["2"],
        ),
        (
            ["1", "2", "3"],
            [0, 1, 0],
            2,
            False,
            False,
            ["2", "3"],
        ),
        (
            ["1", "2", "3"],
            [0, 1, 0],
            4,
            False,
            False,
            ["2", "3", "1", "2"],
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{user_id_active}>"],
            [1, 0],
            3,
            True,
            False,
            [f"<@{user_id_active}>", f"<@{user_id_active}>", f"<@{user_id_active}>"],
        ),
        (
            [user_id_inactive, f"<@{user_id_active}>"],
            [1, 0],
            3,
            True,
            False,
            [user_id_inactive, f"<@{user_id_active}>", user_id_inactive],
        ),
        (
            [f"<@{user_id_inactive}>", f"<@{current_user_id}>"],
            [1, 0],
            2,
            False,
            True,
            [f"<@{user_id_inactive}>", f"<@{user_id_inactive}>"],
        ),
    ],
)
def test_round_robin_select(
    pick_list: list[str],
    weight_list: list[float],
    number_of_items_to_select: int,
    only_active_users: bool,
    self_exclude: bool,
    expected_items,
    set_seed,
):
    strategy = RoundRobinStrategy(pick_list=pick_list, weight_list=weight_list)
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
def test_round_robin_select_errors(
    pick_list, weight_list, self_exclude, only_active_users, error_message
):
    strategy = RoundRobinStrategy(pick_list=pick_list, weight_list=weight_list)
    with pytest.raises(MissingElementError, match=error_message):
        strategy.select(
            number_of_items_to_select=1,
            self_exclude=self_exclude,
            user_id=current_user_id,
            only_active_users=only_active_users,
            team_id=team_id,
        )
