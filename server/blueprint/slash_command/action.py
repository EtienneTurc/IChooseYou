from enum import Enum


class BlueprintSlashCommandAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RANDOMNESS = "randomness"
    XMAS_CELEBRATION = "xmas_celebration"
    XMAS = "xmas"
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
        BlueprintSlashCommandAction.RANDOMNESS,
        BlueprintSlashCommandAction.INSTANT,
        BlueprintSlashCommandAction.CLEAN_DELETED_USERS,
    ]
]

XMAS_SLASH_COMMANDS = [
    action.value
    for action in BlueprintSlashCommandAction
    if action
    in [BlueprintSlashCommandAction.XMAS_CELEBRATION, BlueprintSlashCommandAction.XMAS]
]
