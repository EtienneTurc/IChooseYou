import numpy as np
cimport numpy as np
import math
cimport cython

np.import_array()

COLOR_TYPE = np.uint8
ctypedef np.uint8_t COLOR_t
ctypedef np.double_t SECTION_t

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def create_frame(np.ndarray[SECTION_t, ndim=2] sections, np.ndarray[COLOR_t, ndim=2] colors, np.ndarray[double, ndim=2] angle_matrix, int width, int height, int radius, int center_x, int center_y, int triangle_size):

    cdef np.ndarray[COLOR_t, ndim=3] frame = np.ones((height, width, 3), dtype=COLOR_TYPE) * 255

    cdef int x_distance, y_distance, distance_from_center, i, x, y, x_distance_from_left_edge, y_distance_from_center
    cdef double x_angle, angle

    cdef SECTION_t section_start_angle, section_end_angle

    cdef int len_sections = len(sections)
    cdef double pi = math.pi

    for x in range(width):
        for y in range(height):
            x_distance_from_left_edge = width - x
            y_distance_from_center = center_y - y

            if y_distance_from_center < 0:
                y_distance_from_center = - y_distance_from_center

            # Triangle section
            if x_distance_from_left_edge + y_distance_from_center < triangle_size:
                frame[y, x, 0] = 0
                frame[y, x, 1] = 0
                frame[y, x, 2] = 0
                continue

            x_distance = x - center_x
            y_distance = y - center_y

            distance_from_center = x_distance**2 + y_distance**2

            if distance_from_center < 10:
                frame[y, x, 0] = 0
                frame[y, x, 1] = 0
                frame[y, x, 2] = 0
                continue

            if distance_from_center > radius**2 or distance_from_center < 50:
                continue

            x_angle = angle_matrix[x, y]

            angle = x_angle
            if y_distance < 0:
                angle = 2 * pi  - x_angle

            for i in range(len_sections):
                section_start_angle = sections[i, 0]
                section_end_angle = sections[i, 1]
                if (
                    section_start_angle <= angle
                    and section_end_angle > angle
                    or (section_start_angle > section_end_angle
                    and (section_start_angle <= angle
                    or section_end_angle > angle))
                ):
                    frame[y, x, 0] = colors[i, 0]
                    frame[y, x, 1] = colors[i, 1]
                    frame[y, x, 2] = colors[i, 2]
                    break;
    return frame
