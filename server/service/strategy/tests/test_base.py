import pytest

from server.service.error.type.consistency_error import ConsistencyError
from server.service.strategy.base import BaseStrategy

default_pick_list = ["1", "2", "3", "4", "5", "6"]


def test_base_create_weight_list():
    assert BaseStrategy.create_weight_list(3) == [1 / 3, 1 / 3, 1 / 3]


def test_base_strategy_creation():
    weight_list = [1 / 3, 2 / 3]
    strategy = BaseStrategy(
        pick_list=default_pick_list[: len(weight_list)], weight_list=weight_list
    )
    assert strategy.weight_list == weight_list


def test_base_strategy_creation_round_sum():
    weight_list = [0.999999999999]
    try:
        BaseStrategy(
            pick_list=default_pick_list[: len(weight_list)], weight_list=weight_list
        )
    except Exception:
        pytest.fail("Should not fail even if the weight list is not exactly 1")


@pytest.mark.parametrize(
    "pick_list, weight_list, error_message",
    [
        ([], [1], "Can't pick an item from an empty pick list."),
        (default_pick_list, [], "Weight list must not be empty."),
        (
            default_pick_list,
            [1],
            "Pick list and weight list muse have the same length.",
        ),
        (default_pick_list[:2], [1, 2], "Weight list must sum up to 1."),
    ],
)
def test_base_strategy_creation_error(pick_list, weight_list, error_message):
    with pytest.raises(ConsistencyError, match=error_message):
        BaseStrategy(pick_list=pick_list, weight_list=weight_list)


@pytest.mark.parametrize(
    "items_to_add, value, expected_weight_list",
    [
        ([], None, [1 / 3, 2 / 3]),
        (["c"], None, [2 / 9, 4 / 9, 3 / 9]),
        (["c"], 1, [1 / 6, 1 / 3, 1 / 2]),
        (["c"], 0, [1 / 3, 2 / 3, 0]),
        (["c", "d"], None, [2 / 12, 4 / 12, 3 / 12, 3 / 12]),
    ],
)
def test_base_strategy_add_items(items_to_add, value, expected_weight_list):
    weight_list = [1 / 3, 2 / 3]
    strategy = BaseStrategy(
        pick_list=default_pick_list[: len(weight_list)], weight_list=weight_list
    )
    strategy.add_items(items_to_add, value)
    assert strategy.pick_list == default_pick_list[: len(weight_list)] + items_to_add
    assert [round(el, 6) for el in strategy.weight_list] == [
        round(el, 6) for el in expected_weight_list
    ]


@pytest.mark.parametrize(
    "items_indices, expected_pick_list, expected_weight_list",
    [
        ([], default_pick_list[:3], [1 / 6, 2 / 6, 3 / 6]),
        ([0], default_pick_list[1:3], [2 / 5, 3 / 5]),
        ([1], [default_pick_list[0], default_pick_list[2]], [1 / 4, 3 / 4]),
        ([2], default_pick_list[:2], [1 / 3, 2 / 3]),
        ([0, 1], [default_pick_list[2]], [1]),
    ],
)
def test_base_strategy_remove_item(
    items_indices, expected_pick_list, expected_weight_list
):
    pick_list = default_pick_list[:3]
    weight_list = [1 / 6, 2 / 6, 3 / 6]
    strategy = BaseStrategy(pick_list=pick_list, weight_list=weight_list)
    strategy.remove_items(items_indices)
    assert strategy.pick_list == expected_pick_list
    assert [round(el, 6) for el in strategy.weight_list] == [
        round(el, 6) for el in expected_weight_list
    ]
