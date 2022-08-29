def flatten(t):
    return [item for sublist in t for item in sublist]


def format_list_to_string(list_to_format: list[any]) -> list[any]:
    if len(list_to_format) == 1:
        return list_to_format[0]

    left_items = list_to_format[:-1]
    right_item = list_to_format[-1]

    left = ", ".join(left_items)
    right = f" and {right_item}"

    return left + right
