import pytest

from server.service.strategy.round_robin import RoundRobinStrategy


def test_base_create_weight_list():
    assert RoundRobinStrategy.create_weight_list(3) == [1, 0, 0]


@pytest.mark.parametrize(
    "initial_weight_list, indices_selected, expected_weight_list",
    [
        ([1, 0, 0, 0], [0], [0, 1, 0, 0]),
        ([0, 1, 0, 0], [1], [0, 0, 1, 0]),
        ([0, 0, 1, 0], [2], [0, 0, 0, 1]),
        ([0, 0, 0, 1], [3], [1, 0, 0, 0]),
        ([0, 1, 0, 0], [1, 2], [0, 0, 0, 1]),
        ([0, 1, 0, 0], [1, 3], [1, 0, 0, 0]),
    ],
)
def test_round_robin_update(
    initial_weight_list, indices_selected, expected_weight_list
):
    result = RoundRobinStrategy(weight_list=initial_weight_list).update(
        indices_selected=indices_selected
    )
    assert result == expected_weight_list


@pytest.mark.parametrize(
    "number_of_items_to_add, weight_list, expected_weight_list",
    [
        (1, [1, 0], [1, 0, 0]),
        (2, [1, 0], [1, 0, 0, 0]),
        (2, [0, 1], [0, 1, 0, 0]),
    ],
)
def test_round_robin_add_items(
    number_of_items_to_add, weight_list, expected_weight_list
):
    strategy = RoundRobinStrategy(weight_list=weight_list)
    strategy.add_items(number_of_items_to_add)
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
    strategy = RoundRobinStrategy(weight_list=weight_list)
    strategy.remove_items(indices)
    assert strategy.weight_list == expected_weight_list
