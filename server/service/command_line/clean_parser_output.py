import functools
import re


def get_as_string(value) -> str:
    if not value:
        return ""
    if type(value) == list:
        return (" ").join(value)
    return value


def get_as_bool(value: bool) -> str:
    if value is None:
        return None

    if type(value) is bool:
        return value

    return False if value is False or str.lower(value) == "false" else True


def get_as_list(value, *, clean_mentions):
    if not value:
        return []

    option_list = []
    for word_of_char in value:
        word = "".join(word_of_char)
        if clean_mentions:
            word = clean_mention(word)
        option_list.append(word)
    return option_list


def options_to_dict(options, args):
    args_dict = {arg.variable_name: arg for arg in args}
    options_dict = {}
    for option_name in options:
        arg = args_dict[option_name]
        value = options[option_name]
        func_to_apply = get_as_string
        if arg.type == bool:
            func_to_apply = get_as_bool
        elif arg.type == list:
            func_to_apply = functools.partial(
                get_as_list,
                clean_mentions=arg.clean_mentions,
            )

        options_dict[option_name] = func_to_apply(value)
    return options_dict


def clean_mention(text: str) -> str:
    if not text:
        return text
    return re.sub(r"<(@U[A-Z0-9]*)\|(.*?)>", r"<\1>", text)


def clean_empty_fields(d: dict[str, any]) -> dict[str, any]:
    new_dict = {}
    for key in d:
        el = d[key]
        if not (el is None or el == "" or el == []):
            new_dict[key] = el
    return new_dict
