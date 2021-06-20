def pick(dict, elements):
    new_dict = {}
    for el in elements:
        new_dict[el] = dict.get(el)
    return new_dict
