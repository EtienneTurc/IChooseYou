from enum import Enum


class BlueprintSlashCommandAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RANDOMNESS = "randomness"
    CUSTOM = "custom"


KNOWN_SLASH_COMMANDS_ACTIONS = [
    action.value
    for action in BlueprintSlashCommandAction
    if action is not BlueprintSlashCommandAction.CUSTOM
]
