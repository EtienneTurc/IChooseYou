from enum import Enum


class BlueprintSlashCommandAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RANDOMNESS = "randomness"
    INSTANT = "instant"
    CUSTOM = "custom"
    OPEN_MAIN_MODAl = "open_main_modal"
    CLEAN_DELETED_USERS = "clean_deleted_users"


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
        BlueprintSlashCommandAction.CLEAN_DELETED_USERS,
    ]
]
