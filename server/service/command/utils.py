import functools
import re
import random

from server.service.slack.message_formatting import format_mention_user
from server.service.slack.request import get_users_in_channel
from server.service.command.enum import PickListSpecialArg
from server.service.slack.request import is_user_of_team_active


def get_as_string(value, *, nargs0or1) -> str:
    if not value:
        return ""
    if nargs0or1:
        return value
    return (" ").join(value)


def get_as_bool(value: bool) -> str:
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
    print(options)
    print(args)
    args_dict = {arg.variable_name: arg for arg in args}
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
    if pick_list == [PickListSpecialArg.ALL_MEMBERS.value]:
        pick_list = []
        members = get_users_in_channel(team_id, channel_id)
        return [format_mention_user(member_id) for member_id in members]
    return pick_list


def format_examples(
    slash_command: str, command_name: str, examples: list[str]
) -> list[str]:
    return [f"{slash_command} {command_name} {example}" for example in examples]


def clean_mention(text: str) -> str:
    if not text:
        return text
    return re.sub(r"<(@U[A-Z0-9]*)\|(.*?)>", r"<\1>", text)


def is_mention(text: str) -> bool:
    return text and text.startswith("<@") and text.endswith(">")


def get_user_id_in_mention(text: str) -> int:
    text_clean = text[2:-1]
    return text_clean.split("|")[0]


def select_from_pick_list(
    pick_list: list[str], team_id: int, only_active_users: bool = False
) -> str:
    if not pick_list or not len(pick_list):
        return None

    selected_element = random.choice(pick_list)

    print(only_active_users)

    if not only_active_users:
        return selected_element

    if not is_mention(selected_element):
        return selected_element

    user_mentionned = get_user_id_in_mention(selected_element)
    if is_user_of_team_active(team_id, user_mentionned):
        return selected_element

    new_pick_list = [el for el in pick_list if el != selected_element]
    return select_from_pick_list(
        new_pick_list, team_id, only_active_users=only_active_users
    )
