from server.orm.command import Command
from server.service.command.custom.helper import (assert_pick_list, assert_selected_items,
                                                  create_custom_command_label)
from server.service.command.custom.schema import CustomCommandProcessorSchema
from server.service.helper.dict_helper import normalize
from server.service.selection.selection import select_from_pick_list
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_message
from server.service.strategy.helper import get_strategy
from server.service.validator.decorator import validate_schema


@validate_schema(CustomCommandProcessorSchema)
def custom_command_processor(
    *,
    user_id: str,
    team_id: str,
    channel_id: str,
    command_name: str,
    additional_text: str = "",
    number_of_items_to_select: int = 1,
    should_update_weight_list: bool = False,
) -> dict[str, any]:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    pick_list = command.pick_list
    weight_list = command.weight_list

    if command.self_exclude and user_id:
        indices_of_items_to_remove = [
            index for index, item in enumerate(command.pick_list) if user_id in item
        ]
        pick_list = [
            item
            for index, item in enumerate(command.pick_list)
            if index not in indices_of_items_to_remove
        ]
        weight_list = normalize(
            [
                item
                for index, item in enumerate(command.weight_list)
                if index not in indices_of_items_to_remove
            ]
        )

    assert_pick_list(pick_list, len(pick_list) != len(command.pick_list))

    selected_items = select_from_pick_list(
        pick_list,
        weight_list,
        command.strategy,
        number_of_items_to_select=number_of_items_to_select,
        team_id=team_id,
        only_active_users=command.only_active_users,
    )
    assert_selected_items(selected_items, command.only_active_users, command_name)

    label = create_custom_command_label(command.label, additional_text)

    if should_update_weight_list:
        update_weight_list(command, selected_items)

    return {
        "message": Message(
            content=format_custom_command_message(user_id, selected_items, label),
            visibility=MessageVisibility.NORMAL,
            as_attachment=False,
        ),
        "selected_items": selected_items,
    }


def update_weight_list(command: Command, selected_items: list[str]) -> None:
    strategy = get_strategy(command.strategy, command.weight_list)
    strategy.update(
        indices_selected=[
            command.pick_list.index(selected_item) for selected_item in selected_items
        ]
    )
    Command.update(
        command.name,
        command.channel_id,
        command.updated_by_user_id,
        {"weight_list": strategy.weight_list},
    )
