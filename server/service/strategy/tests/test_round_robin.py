import pytest

from server.service.strategy.round_robin import RoundRobinStrategy


@pytest.mark.parametrize(
    "initial_weight_list, expected_weight_list",
    [
        ([1, 0, 0, 0], [0, 1, 0, 0]),
        ([0, 1, 0, 0], [0, 0, 1, 0]),
        ([0, 0, 1, 0], [0, 0, 0, 1]),
        ([0, 0, 0, 1], [1, 0, 0, 0]),
    ],
)
def test_round_robin_update(initial_weight_list, expected_weight_list):
    result = RoundRobinStrategy(weight_list=initial_weight_list).update()
    assert result == expected_weight_list
