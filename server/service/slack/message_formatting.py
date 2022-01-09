import re

from server.blueprint.interactivity.action import BlueprintInteractivityAction
from server.service.helper.dict_helper import get_by_path
from server.service.slack.sdk_helper import get_user_info


def format_custom_command_message(
    user_id: str, selected_items: list[str], label: str
) -> str:
    selected_items_msg = format_custom_selected_items(selected_items)
    return f"Hey ! {format_mention_user(user_id)} choose {selected_items_msg} {label}"


def format_custom_selected_items(selected_items: list[str]) -> str:
    if len(selected_items) == 1:
        return selected_items[0]

    left_items = selected_items[:-1]
    right_item = selected_items[-1]

    left = ", ".join(left_items)
    right = f" and {right_item}"

    return left + right


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
    current_user_name = get_by_path(
        get_user_info(team_id=team_id, user_id=current_user_id), "profile.display_name"
    )
    message = f"{current_user_name} created *{command_name}*."
    if command_description:
        message += f"\n{command_description}"
    message += (
        f"\nUsers in the pick list are: {format_pick_list_users(pick_list, team_id)}."
    )
    return message


def format_command_sent(slash_command, command_name, text):
    command = f"{command_name} {text}"
    return {
        "attachments": [
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": slash_command + " " + command,
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Resubmit command",
                                "emoji": True,
                            },
                            "value": command,
                            "action_id": BlueprintInteractivityAction.RESUBMIT_COMMAND.value,  # noqa E501
                        },
                    }
                ]
            }
        ]
    }


def format_updated_fields_mesage(
    *,
    command_name: str,
    team_id: str,
    fields_updated: dict[str, any],
    current_user_id: str,
) -> str:
    current_user_name = get_by_path(
        get_user_info(team_id=team_id, user_id=current_user_id), "profile.display_name"
    )
    message = f"{current_user_name} updated *{command_name}*."

    messages_for_each_field = [
        ("name", (lambda name: f"Command name changed to {name}.")),
        (
            "added_to_pick_list",
            (
                lambda added_to_pick_list: f"New users added: {format_pick_list_users(added_to_pick_list, team_id)}."  # noqa E501
            ),
        ),
        (
            "removed_from_pick_list",
            lambda removed_from_pick_list: f"Users removed: {format_pick_list_users(removed_from_pick_list, team_id)}.",  # noqa E501
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


def format_pick_list_users(users_mention: list[str], team_id: str) -> str:
    user_infos = [
        get_by_path(
            get_user_info(team_id=team_id, user_id=get_user_id_from_mention(user)),
            "profile.display_name",
        )
        or user
        for user in users_mention
    ]
    return format_custom_selected_items(user_infos)
