def format_known_command_help(known_commands):
    message = f"{known_commands.name}: {known_commands.description}.\n"
    for arg in known_commands.args:
        message += f"{len(known_commands.name) * ' '}  {arg.name}: {arg.help}\n"
    return message


def format_known_commands_help(known_commands):
    message = ""
    for command in known_commands:
        args_names = " ".join([f"--{arg.name}" for arg in command.args])
        message += f"{command.name}: {command.description}.\n"
        message += f"{len(command.name) * ' '}  Args: {args_names}."
    return message


def format_custom_command_message(user, selected_element, label):
    return f"Hey ! {format_mention(user)} choose {selected_element} to {label}"


def format_mention(user):
    if not user or not user.get("id") or not user.get("name"):
        return "user"
    return f"<@{user['id']}|{user['name']}>"


def format_custom_command_help(custom_command):
    self_exclude = "not" if not custom_command.self_exclude else ""
    slack_message_from_command = format_custom_command_message(
        None, "selected_element", custom_command.label
    )

    message = f"{custom_command.name}:"
    message += f"- Message: {slack_message_from_command}"
    message += f"- Pick list: {custom_command.pick_list}"
    message += f"- User using the slash command {self_exclude} excluded."

    return message


def format_custom_commands_help(custom_commands):
    message = ""
    for custom_command in custom_commands:
        slack_message_from_command = format_custom_command_message(
            None, "selected_element", custom_command.label
        )
        message += f"{custom_command.name}: {slack_message_from_command}.\n"
    return message
