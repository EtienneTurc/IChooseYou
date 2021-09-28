from server.service.command.enum import PickListSpecialArg
from server.service.slack.message_formatting import format_mention_user
from server.service.slack.sdk_wrapper import get_users_in_channel


def format_pick_list(pick_list: list[str], team_id: str, channel_id: str) -> list[str]:
    if pick_list == [PickListSpecialArg.ALL_MEMBERS.value]:
        pick_list = []
        members = get_users_in_channel(team_id, channel_id)
        return [format_mention_user(member_id) for member_id in members]
    return pick_list
