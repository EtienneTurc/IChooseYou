from enum import Enum


class BlueprintSlashCommandAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RANDOMNESS = "randomness"
    INSTANT = "instant"
    CUSTOM = "custom"
    OPEN_MAIN_MODAl = "open_main_modal"


KNOWN_SLASH_COMMANDS_ACTIONS = [
    action.value
    for action in BlueprintSlashCommandAction
    if action
    in [
        BlueprintSlashCommandAction.CREATE,
        BlueprintSlashCommandAction.UPDATE,
        BlueprintSlashCommandAction.DELETE,
        BlueprintSlashCommandAction.INSTANT,
        BlueprintSlashCommandAction.RANDOMNESS,
    ]
]
