def create_custom_command_label(command_label: str, additional_text: str) -> str:
    space = " " if command_label and additional_text else ""
    return f"{command_label}{space}{additional_text}"
