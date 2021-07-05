import numpy as np


def pick(dict, elements):
    new_dict = {}
    for el in elements:
        new_dict[el] = dict.get(el)
    return new_dict


def get_by_path(dict, path: str):
    keys = path.split(".")
    value = dict
    for key in keys:
        if value is None:
            return None
        value = value.get(key)
    return value


def normalize(input_list: list[float]) -> list[float]:
    return list(np.array(input_list) / np.sum(input_list))
