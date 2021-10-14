import re

from server.blueprint.interactivity.action import BlueprintInteractivityAction


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


def format_custom_command_help(custom_command):
    self_exclude = "not " if not custom_command.self_exclude else ""
    only_active_users = (
        "Only active users" if custom_command.only_active_users else "All items"
    )
    slack_message_from_command = format_custom_command_message(
        None, ["<selected_item>"], custom_command.label
    )

    message = f"*{custom_command.name}*: {custom_command.description}"
    message += f"\n• Message: {slack_message_from_command}"
    message += f"\n• Pick list: {custom_command.pick_list}"
    message += f"\n• Strategy: {custom_command.strategy}."
    message += f"\n• User using the slash command {self_exclude}excluded."
    message += f"\n• {only_active_users} are selected when using the slash command."

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
