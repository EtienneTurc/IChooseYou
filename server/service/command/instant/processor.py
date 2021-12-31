from server.service.command.helper import format_pick_list
from server.service.command.instant.helper import assert_selected_items
from server.service.command.instant.schema import InstantCommandProcessorSchema
from server.service.selection.selection import clean_and_select_from_pick_list
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_message
from server.service.strategy.enum import Strategy
from server.service.validator.decorator import validate_schema


@validate_schema(InstantCommandProcessorSchema)
def instant_command_processor(
    *,
    user_id: str,
    team_id: str,
    channel_id: str,
    label: str = "",
    pick_list: list[str],
    number_of_items_to_select: int = 1,
    only_active_users: bool = False,
) -> dict[str, any]:
    pick_list = format_pick_list(pick_list, team_id, channel_id)
    strategy = Strategy.uniform
    weight_list = strategy.value.create_weight_list(len(pick_list))

    selected_items = clean_and_select_from_pick_list(
        pick_list=pick_list,
        weight_list=weight_list,
        user_id=user_id,
        strategy_name=strategy.name,
        number_of_items_to_select=number_of_items_to_select,
        team_id=team_id,
        only_active_users=only_active_users,
        self_exclude=False,
    )
    assert_selected_items(selected_items, only_active_users)

    return {
        "message": Message(
            content=format_custom_command_message(user_id, selected_items, label),
            visibility=MessageVisibility.NORMAL,
            as_attachment=False,
        ),
        "selected_items": selected_items,
        "number_of_items_to_select": number_of_items_to_select,
    }
