import math

import pytest

from server.service.wheel.builder import (build_wheel, compute_angles,
                                          proportions_to_sections)
from server.service.wheel.constant import (LEGEND_WIDTH, NB_FRAMES, WHEEL_HEIGHT,
                                           WHEEL_WIDTH)


@pytest.mark.parametrize(
    "proportions, initial_angle, expected_sections",
    [
        ([1], 0, [[0, 0]]),
        (
            [0.25, 0.25, 0.5],
            0,
            [[0, math.pi / 2], [math.pi / 2, math.pi], [math.pi, 0]],
        ),
        ([0.25, 0.75], math.pi / 2, [[math.pi / 2, math.pi], [math.pi, math.pi / 2]]),
    ],
)
def test_proportions_to_sections(proportions, initial_angle, expected_sections):
    sections = proportions_to_sections(proportions, initial_angle)
    assert len(sections) == len(expected_sections)
    for i, section in enumerate(sections):
        assert section[0] == expected_sections[i][0]
        assert section[1] == expected_sections[i][1]


@pytest.mark.parametrize(
    "nb_frames, end_section, expected_number_of_turn",
    [
        (2, [math.pi / 2, math.pi], 5),
        (4, [math.pi / 2, math.pi], 5),
        (100, [math.pi / 2, math.pi], 5),
    ],
)
def test_compute_angles(nb_frames, end_section, expected_number_of_turn):
    angles = compute_angles(nb_frames, end_section)
    last_angle = angles[-1]
    assert last_angle >= (expected_number_of_turn * 2 * math.pi) + (
        2 * math.pi - end_section[1]
    )
    assert last_angle <= (expected_number_of_turn * 2 * math.pi) + (
        2 * math.pi - end_section[0]
    )


@pytest.mark.parametrize(
    "proportion_size, expected_width",
    [
        (1, WHEEL_WIDTH + LEGEND_WIDTH),
        (10, WHEEL_WIDTH + 2 * LEGEND_WIDTH),
        (20, WHEEL_WIDTH + 3 * LEGEND_WIDTH),
        (30, WHEEL_WIDTH + 3 * LEGEND_WIDTH),
    ],
)
def test_build_wheel(proportion_size, expected_width):
    proportions = [1 / proportion_size] * proportion_size
    names = ["&"] * proportion_size
    selected_name = names[0]
    wheel = build_wheel(
        proportions,
        names,
        selected_name,
    )
    assert wheel.shape == (NB_FRAMES, WHEEL_HEIGHT, expected_width, 3)
