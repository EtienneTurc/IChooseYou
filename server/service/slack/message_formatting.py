def format_known_command_help(known_command):
    command = known_command(text=None, team_id=None, channel_id=None)
    message = f"*{command.name}*: {command.description}.\n"
    message += "_Arguments_:\n"
    for arg in command.args:
        message += f"• *{arg.name}*: {arg.help}\n"
    message += f"_Usage_: {command.usage}"
    message += f"{format_examples(command.examples)}"
    return message


def format_known_commands_help(known_commands):
    message = ""
    for command_class in known_commands:
        command = command_class(text=None, team_id=None, channel_id=None)
        message += f"*{command.name}*: {command.description}.\n"
        message += f"Usage: {command.usage}"
        message += f"{format_examples(command.examples)}"
    return message


def format_custom_command_message(user, selected_element, label):
    return f"Hey ! {format_mention_user(user)} choose {selected_element} {label}"


def format_mention_user(user):
    if not user or not user.get("id"):
        return "<@user>"
    return f"<@{user['id']}>"


def format_custom_command_help(custom_command):
    self_exclude = "not " if not custom_command.self_exclude else ""
    slack_message_from_command = format_custom_command_message(
        None, "<selected_element>", custom_command.label
    )

    message = f"*{custom_command.name}*:"
    message += f"\n• Message: {slack_message_from_command}"
    message += f"\n• Pick list: {custom_command.pick_list}"
    message += f"\n• User using the slash command {self_exclude}excluded."

    return message


def format_custom_commands_help(custom_commands):
    message = ""
    for custom_command in custom_commands:
        slack_message_from_command = format_custom_command_message(
            None, "selected_element", custom_command.label
        )
        message += f"• *{custom_command.name}*: {slack_message_from_command}.\n"
    return message


def format_examples(examples):
    message = "> Examples:\n"
    for example in examples:
        message += f"> `{example}`\n"
    return message