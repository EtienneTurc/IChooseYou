from marshmallow import ValidationError

from server.service.command.enum import PickListSpecialArg
from server.service.slack.message_formatting import format_mention_user
from server.service.slack.sdk_helper import get_users_in_channel
from server.service.strategy.enum import Strategy


def format_pick_list(pick_list: list[str], team_id: str, channel_id: str) -> list[str]:
    if pick_list == [PickListSpecialArg.ALL_MEMBERS.value]:
        pick_list = []
        members = get_users_in_channel(team_id=team_id, channel_id=channel_id)
        return [format_mention_user(member_id) for member_id in members]
    return pick_list


def assert_strategy_is_valid(strategy_name: str) -> None:
    if strategy_name and strategy_name not in Strategy._member_names_:
        error_message = f"{strategy_name} is not a valid strategy."
        error_message += (
            f"\nValid strategies are: {', '.join(Strategy._member_names_)}."
        )
        raise ValidationError(error_message)
