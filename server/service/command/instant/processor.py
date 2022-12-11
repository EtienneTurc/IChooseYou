from server.orm.channel import Channel
from server.service.command.helper import format_pick_list
from server.service.command.instant.schema import InstantCommandProcessorSchema
from server.service.slack.message import Message, MessageVisibility
from server.service.slack.message_formatting import (extract_label_from_pick_list,
                                                     format_custom_command_message)
from server.service.strategy.uniform import UniformStrategy
from server.service.validator.decorator import validate_schema
from server.service.wheel.builder import build_wheel


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
    with_wheel: bool = False,
) -> dict[str, any]:
    pick_list = format_pick_list(pick_list, team_id, channel_id)
    weight_list = UniformStrategy.create_weight_list(len(pick_list))
    strategy = UniformStrategy(pick_list=pick_list, weight_list=weight_list)

    selected_items = strategy.select(
        number_of_items_to_select=number_of_items_to_select,
        self_exclude=False,
        user_id=user_id,
        only_active_users=only_active_users,
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

    use_santa_in_message = Channel.find_one_by_channel_id(
        channel_id
    ).found_xmas_easter_egg

    return {
        "message": Message(
            content=format_custom_command_message(
                user_id, selected_items, label, use_santa_in_message
            ),
            visibility=MessageVisibility.NORMAL,
            as_attachment=False,
        ),
        "selected_items": selected_items,
        "gif_frames": gif_frames,
        "with_wheel": with_wheel,
        "number_of_items_to_select": number_of_items_to_select,
    }
