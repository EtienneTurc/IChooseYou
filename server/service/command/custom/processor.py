from server.orm.command import Command
from server.service.command.custom.helper import create_custom_command_label
from server.service.command.custom.schema import CustomCommandProcessorSchema
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
    should_update_command: bool = False,
    with_wheel: bool = False,
) -> dict[str, any]:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    strategy = get_strategy(
        command.strategy,
        pick_list=command.pick_list,
        weight_list=command.weight_list,
    )

    selected_items = strategy.select(
        number_of_items_to_select=number_of_items_to_select,
        self_exclude=command.self_exclude,
        user_id=user_id,
        only_active_users=command.only_active_users,
        team_id=team_id,
    )
    cleaned_pick_list, cleaned_weight_list = strategy.get_clean_lists()

    gif_frames = None
    if with_wheel:
        labels = extract_label_from_pick_list(cleaned_pick_list, team_id=team_id)
        gif_frames = build_wheel(
            cleaned_weight_list,
            labels,
            labels[cleaned_pick_list.index(selected_items[0])],
        )
    label = create_custom_command_label(command.label, additional_text)

    if should_update_command:
        update_command(command, selected_items)

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


def update_command(command: Command, selected_items: list[str]) -> None:
    strategy = get_strategy(
        command.strategy, pick_list=command.pick_list, weight_list=command.weight_list
    )
    strategy.update(
        indices_selected=[
            command.pick_list.index(selected_item) for selected_item in selected_items
        ]
    )
    Command.update(
        command.name,
        command.channel_id,
        command.updated_by_user_id,
        {"pick_list": strategy.pick_list, "weight_list": strategy.weight_list},
    )
