import pytest

from server.service.strategy.smooth import SmoothStrategy


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
    result = SmoothStrategy(weight_list=initial_weight_list).update(
        indices_selected=indices_selected
    )
    assert [round(el, 6) for el in result] == [
        round(el, 6) for el in expected_weight_list
    ]
