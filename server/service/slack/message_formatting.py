import re

from server.service.helper.dict_helper import get_by_path
from server.service.helper.list_helper import format_list_to_string
from server.service.slack.sdk_helper import get_user_info


def format_custom_command_message(
    user_id: str, selected_items: list[str], label: str
) -> str:
    selected_items_msg = format_list_to_string(selected_items)
    return f"Hey ! {format_mention_user(user_id)} choose {selected_items_msg} {label}"


def format_mention_user(user_id: str) -> str:
    if not user_id:
        return "<@user>"
    return f"<@{user_id}>"


def get_user_id_from_mention(text: str) -> str:
    if not text:
        return text
    return re.sub(r"<@(U[A-Z0-9]*)(\|.*)*>", r"\1", text)


def format_new_command_message(
    *,
    command_name: str,
    team_id: str,
    command_description: str,
    pick_list: list[str],
    current_user_id: str,
):
    current_user_name = get_name_from_user(
        get_user_info(team_id=team_id, user_id=current_user_id),
    )
    message = f"{current_user_name} created *{command_name}*."
    if command_description:
        message += f"\n{command_description}"

    message += "\nItems in the pick list are: "

    message += format_pick_list(pick_list, team_id) + "."
    return message


def format_updated_fields_mesage(
    *,
    command_name: str,
    team_id: str,
    fields_updated: dict[str, any],
    current_user_id: str,
) -> str:
    current_user_name = get_name_from_user(
        get_user_info(team_id=team_id, user_id=current_user_id),
    )
    message = f"{current_user_name} updated *{command_name}*."

    messages_for_each_field = [
        ("name", (lambda name: f"Command name changed to {name}.")),
        (
            "added_to_pick_list",
            (
                lambda added_to_pick_list: f"New items added: {format_pick_list(added_to_pick_list, team_id)}."  # noqa E501
            ),
        ),
        (
            "removed_from_pick_list",
            lambda removed_from_pick_list: f"Items removed: {format_pick_list(removed_from_pick_list, team_id)}.",  # noqa E501
        ),
        (
            "description",
            (
                lambda description: f"Command description changed to: {description}."
                if description
                else "Command description removed."
            ),
        ),
        (
            "label",
            (
                lambda label: f'Command message changed to: {format_custom_command_message(None, ["<selected_item>"], label)}'  # noqa E501
            ),
        ),
        (
            "self_exclude",
            (
                lambda self_exclude: f'User running the command is now {"excluded" if self_exclude else "included"} in the pick.'  # noqa E501
            ),
        ),
        (
            "only_active_users",
            (
                lambda only_active_users: "Only active users are now picked."
                if only_active_users
                else "All users are now picked (whether or not they are active)."
            ),
        ),
        ("strategy", (lambda strategy: f"Strategy changed to {strategy}.")),
    ]

    for (field, message_function) in messages_for_each_field:
        if fields_updated.get(field) is not None:
            message += f"\n• {message_function(fields_updated.get(field))}"

    return message


def format_clean_deleted_users_message(*, current_user_id: str, team_id: str):
    current_user_name = get_name_from_user(
        get_user_info(team_id=team_id, user_id=current_user_id),
    )
    return (
        f"{current_user_name} cleaned up the deleted users from the pick lists :broom:"
    )


def format_no_deleted_users_to_clean_message():
    return "No deleted users found. All pick commands are up to date."


def format_pick_list(pick_list: list[str], team_id: str):
    labels = extract_label_from_pick_list(pick_list, team_id=team_id)
    return format_list_to_string(labels)


def is_a_user(item: str) -> bool:
    return item is not None and item.startswith("<@U") and item.endswith(">")


def get_name_from_user(user: dict[str, any]) -> str:
    possible_path_names = [
        "profile.display_name",
        "profile.display_name_normalized",
        "profile.real_name",
        "profile.real_name_normalized",
        "real_name",
    ]

    for possible_path_name in possible_path_names:
        name = get_by_path(user, possible_path_name)
        if name:
            return name.capitalize()

    return None


def extract_label_from_pick_list(pick_list: list[str], *, team_id: str) -> list[str]:
    if pick_list is None:
        return []
    return [
        transform_pick_list_item_to_label(item, team_id=team_id) for item in pick_list
    ]


def transform_pick_list_item_to_label(item: str, *, team_id: str) -> str:
    if is_a_user(item):
        user_name = get_name_from_user(
            get_user_info(team_id=team_id, user_id=get_user_id_from_mention(item))
        )
        return user_name

    return item
