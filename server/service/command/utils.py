import functools
import re

from server.service.slack.message_formatting import format_mention_user
from server.service.slack.request import get_users_in_channel


def get_as_string(value, *, nargs0or1):
    if not value:
        return ""
    if nargs0or1:
        return value
    return (" ").join(value)


def get_as_bool(value):
    if value is None:
        return None
    return value is True or str(value).lower() == "true"


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
    args_dict = {arg.name: arg for arg in args}
    options_dict = {}
    for option_name in options:
        arg = args_dict[option_name]
        value = options[option_name]
        func_to_apply = functools.partial(
            get_as_string,
            nargs0or1=arg.nargs == "?",
        )
        if arg.type == bool:
            func_to_apply = get_as_bool
        elif arg.type == list:
            func_to_apply = functools.partial(
                get_as_list,
                clean_mentions=arg.clean_mentions,
            )

        options_dict[option_name] = func_to_apply(value)
    return options_dict


def format_text_to_list(text: str) -> list[str]:
    text = text.lstrip()
    text_list = []
    if text:
        text_list = text.split(" ")
    return text_list


def format_pick_list(pick_list: list[str], team_id: int, channel_id: int) -> list[str]:
    if pick_list == ["all_members"]:
        pick_list = []
        members = get_users_in_channel(team_id, channel_id)
        return [format_mention_user(member_id) for member_id in members]
    return pick_list


def format_examples(slash_command, command_name, examples):
    return [f"{slash_command} {command_name} {example}" for example in examples]


def clean_mention(text):
    if not text:
        return text
    return re.sub(r"<(@U[A-Z0-9]*)\|(.*?)>", r"<\1>", text)
