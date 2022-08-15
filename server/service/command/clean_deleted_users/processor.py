from server.orm.command import Command
from server.service.command.clean_deleted_users.schema import \
    CleanDeletedUsersCommandProcessorSchema
from server.service.command.delete.processor import delete_command_processor
from server.service.command.update.processor import update_command_processor
from server.service.slack.helper import get_user_id_in_mention, is_mention
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import (
    format_clean_deleted_users_message, format_no_deleted_users_to_clean_message)
from server.service.slack.sdk_helper import get_user_info
from server.service.validator.decorator import validate_schema


@validate_schema(CleanDeletedUsersCommandProcessorSchema)
def clean_deleted_users_command_processor(
    *, user_id: str, team_id: str, channel_id: str, **kwargs
) -> dict[str, any]:
    commands = Command.find_all_in_chanel(channel_id)

    command_updated = []
    for command in commands:
        deleted_users_in_pick_list = get_deleted_users_in_pick_list(
            command["pick_list"], team_id=team_id
        )
        if len(deleted_users_in_pick_list):
            if len(deleted_users_in_pick_list) == len(command["pick_list"]):
                delete_command_processor(
                    channel_id=channel_id, command_to_delete=command["name"]
                )
            else:
                update_command_processor(
                    user_id=user_id,
                    team_id=team_id,
                    channel_id=channel_id,
                    command_to_update=command["name"],
                    remove_from_pick_list=deleted_users_in_pick_list,
                )
            command_updated.append(command["name"])

    if len(command_updated):
        message_content = format_clean_deleted_users_message(
            current_user_id=user_id, team_id=team_id
        )
        return {
            "message": Message(
                content=message_content,
                status=MessageStatus.INFO,
                visibility=MessageVisibility.NORMAL,
            )
        }

    return {
        "message": Message(
            content=format_no_deleted_users_to_clean_message(),
            status=MessageStatus.INFO,
            visibility=MessageVisibility.HIDDEN,
        )
    }


def get_deleted_users_in_pick_list(pick_list: list[str], *, team_id: str) -> list[str]:
    deleted_users_in_pick_list = []
    for item in pick_list:
        if is_mention(item):
            user_id = get_user_id_in_mention(item)
            user_info = get_user_info(user_id=user_id, team_id=team_id)
            if user_info.get("deleted"):
                deleted_users_in_pick_list.append(item)

    return deleted_users_in_pick_list
