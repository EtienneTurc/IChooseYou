from server.orm.command import Command
from server.service.command.custom.helper import (assert_selected_items,
                                                  create_custom_command_label)
from server.service.command.custom.schema import CustomCommandProcessorSchema
from server.service.selection.selection import clean_and_select_from_pick_list
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import (extract_label_from_pick_list,
                                                     format_custom_command_message)
from server.service.strategy.helper import get_strategy
from server.service.validator.decorator import validate_schema
from server.service.wheel.builder import build_wheel


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
    with_wheel: bool = False,
) -> dict[str, any]:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    pick_list = command.pick_list[:]
    weight_list = command.weight_list[:]

    selected_items = clean_and_select_from_pick_list(
        pick_list=pick_list,
        weight_list=weight_list,
        user_id=user_id,
        strategy_name=command.strategy,
        number_of_items_to_select=number_of_items_to_select,
        team_id=team_id,
        only_active_users=command.only_active_users,
        self_exclude=command.self_exclude,
    )
    assert_selected_items(selected_items, command.only_active_users, command_name)

    gif_frames = None
    if with_wheel:
        labels = extract_label_from_pick_list(pick_list, team_id=team_id)
        gif_frames = build_wheel(
            weight_list, labels, labels[pick_list.index(selected_items[0])]
        )
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
        "additional_text": additional_text,
        "number_of_items_to_select": number_of_items_to_select,
        "gif_frames": gif_frames,
        "with_wheel": with_wheel,
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
