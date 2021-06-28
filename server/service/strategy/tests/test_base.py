import pytest

from server.service.error.back_error import BackError
from server.service.strategy.base import BaseStrategy


def test_base_strategy_creation():
    weight_list = [1 / 3, 2 / 3]
    strategy = BaseStrategy(weight_list=weight_list)
    assert strategy.weight_list == weight_list


@pytest.mark.parametrize(
    "weight_list, error_message",
    [([], "Weight list must not be empty."), ([1, 2], "Weight list must sum up to 1.")],
)
def test_base_strategy_creation_error(weight_list, error_message):
    with pytest.raises(BackError, match=error_message):
        BaseStrategy(weight_list=weight_list)


@pytest.mark.parametrize(
    "value, expected_weight_list",
    [(None, [2 / 9, 4 / 9, 3 / 9]), (1, [1 / 6, 1 / 3, 1 / 2]), (0, [1 / 3, 2 / 3, 0])],
)
def test_base_strategy_add_element(value, expected_weight_list):
    weight_list = [1 / 3, 2 / 3]
    strategy = BaseStrategy(weight_list=weight_list)
    strategy.add_element(value)
    assert [round(el, 6) for el in strategy.weight_list] == [
        round(el, 6) for el in expected_weight_list
    ]


@pytest.mark.parametrize(
    "index_element, expected_weight_list",
    [(0, [2 / 5, 3 / 5]), (1, [1 / 4, 3 / 4]), (2, [1 / 3, 2 / 3])],
)
def test_base_strategy_remove_element(index_element, expected_weight_list):
    weight_list = [1 / 6, 2 / 6, 3 / 6]
    strategy = BaseStrategy(weight_list=weight_list)
    strategy.remove_element(index_element)
    assert [round(el, 6) for el in strategy.weight_list] == [
        round(el, 6) for el in expected_weight_list
    ]
