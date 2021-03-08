from server.command.args import Arg
from server.slack.request import get_users_in_channel
from server.slack.message_formatting import format_mention_member


def find_args_in_text(text):
    text_list = format_text_to_list(text)
    first_arg_index = -1

    named_args = []
    for index, word in enumerate(text_list):
        if word[:2] == "--":
            if first_arg_index == -1:
                first_arg_index = index
            named_args.append(Arg(name=word[2:], nargs="+"))

    positional_args = []
    if first_arg_index == -1:
        first_arg_index = len(text_list)
    for word in text_list[:first_arg_index]:
        positional_args.append(Arg(name=word))

    return positional_args, named_args


def get_args_in_label(label):
    label_list = label.split(" ")
    positional_args = []
    named_args = []
    for word in label_list:
        if word[0] == "$" and word[1:].isdigit():
            positional_args.append(word)
        elif word[0] == "$":
            named_args.append(word)

    return positional_args, named_args


def get_as_string(options, name, nargs0or1):
    value = options[name]
    if not value:
        return ""
    if nargs0or1:
        return value
    return (" ").join(value)


def get_as_bool(options, name, nargs0or1=None):
    if options[name] is None:
        return None
    return options[name] is True or str(options[name]).lower() == "true"


def get_as_list(options, name, nargs0or1=None):
    words_of_chars = options[name]
    if not words_of_chars:
        return []

    option_list = []
    for word_of_char in words_of_chars:
        word = "".join(word_of_char)
        option_list.append(word)
    return option_list


def options_to_dict(options, args):
    args_dict = {arg.name: arg for arg in args}
    options_dict = {}
    for option_name in options:
        func_to_apply = get_as_string
        arg = args_dict[option_name]
        if arg.type == bool:
            func_to_apply = get_as_bool
        elif arg.type == list:
            func_to_apply = get_as_list

        options_dict[option_name] = func_to_apply(
            options, option_name, arg.nargs == "?"
        )
    return options_dict


def format_text_to_list(text):
    text = text.lstrip()
    text_list = []
    if text:
        text_list = text.split(" ")
    return text_list


def format_pick_list(pick_list, channel_id):
    if pick_list == ["all_members"]:
        pick_list = []
        members = get_users_in_channel(channel_id)
        return [format_mention_member(member) for member in members]
    return pick_list
