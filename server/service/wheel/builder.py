import math

import numpy as np

from server.service.wheel.constant import (COLORS, NB_FRAMES, TRIANGLE_SIZE, WHEEL_CENTER,
                                           WHEEL_HEIGHT, WHEEL_RADIUS, WHEEL_WIDTH)
from server.service.wheel.image_helper import build_legend

from create_frame import create_frame  # type: ignore  # isort:skip

FILE_NAME = "main.gif"


def build_wheel(proportions, names, selected_name, colors=COLORS):
    sorted_names, sorted_proportions = sort_by_names(names, proportions)
    selected_index = sorted_names.index(selected_name)
    angles = compute_angles(
        NB_FRAMES, proportions_to_sections(sorted_proportions, 0)[selected_index]
    )
    frames = []
    angle_matrix = compute_angle_matrix()

    # Compute frames
    for angle in angles:
        sections = proportions_to_sections(sorted_proportions, angle)
        frames.append(
            create_frame(
                sections,
                colors,
                angle_matrix,
                WHEEL_WIDTH,
                WHEEL_HEIGHT,
                WHEEL_RADIUS,
                WHEEL_CENTER.x,
                WHEEL_CENTER.y,
                TRIANGLE_SIZE,
            )
        )

    frames_with_legend = add_legend_to_frames(frames, sorted_names, colors)
    return frames_with_legend


def compute_angle_matrix():
    mat = np.zeros((WHEEL_WIDTH, WHEEL_HEIGHT))

    for x in range(WHEEL_WIDTH):
        for y in range(WHEEL_HEIGHT):

            x_distance = x - WHEEL_CENTER.x
            y_distance = y - WHEEL_CENTER.y

            distance_from_center = math.sqrt(x_distance ** 2 + y_distance ** 2)

            if distance_from_center == 0.0:
                continue

            mat[x, y] = math.acos(x_distance / distance_from_center)
    return mat


def proportions_to_sections(proportions, initial_angle):
    sections = []
    for proportion in proportions:
        last_angle = initial_angle % (2 * np.pi)
        if len(sections):
            last_angle = sections[-1][1] % (2 * np.pi)

        portion_angle = proportion * 2 * np.pi
        end_angle = (last_angle + portion_angle) % (2 * np.pi)
        sections.append([last_angle, end_angle])

    return np.array(sections)


def add_legend_to_frames(frames, names, colors):
    legend = build_legend(names, colors)
    full_legend = np.repeat(legend[np.newaxis, :, :], NB_FRAMES, axis=0)
    return np.concatenate((np.array(frames), full_legend), axis=2)


def sort_by_names(names, proportions):
    tuples = [(names[i], proportions[i]) for i in range(len(names))]
    tuples.sort(key=lambda tuple: str.lower(tuple[0]))
    return [t[0] for t in tuples], [t[1] for t in tuples]


def compute_angles(nb_frames, end_section):
    angles = [0]
    for i in range(1, nb_frames):
        value = 1 / (i ** 1.5)
        angles.append(value + angles[i - 1])

    end_section_starting_angle = end_section[0]
    end_section_ending_angle = end_section[1]
    if end_section_starting_angle > end_section_ending_angle:
        end_section_ending_angle += 2 * math.pi

    a = np.random.uniform(
        low=(2 * math.pi - end_section_ending_angle),
        high=(2 * math.pi - end_section_starting_angle),
    )
    end_angle = a + 10 * math.pi

    return (end_angle / angles[-1]) * np.array(angles)
