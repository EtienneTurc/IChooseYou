from server.orm.command import Command
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_help
from server.service.strategy.helper import get_strategy
from server.service.command.update.helper import (
    get_values_to_update,
    get_indices_of_items_to_remove,
    compute_new_pick_list,
    compute_new_weight_list,
    assert_pick_list_can_be_updated,
)
from server.service.command.helper import format_pick_list
from server.service.tpr.response_format import Response
from server.service.slack.response.response_type import SlackResponseType


# @validate_payload TODO Use marshmallow schema instead
def update_command_processor(
    *,
    command_to_update: str,
    label: str = None,
    pick_list: list[str] = None,
    strategy: str = None,
    add_to_pick_list: list[str] = None,
    remove_from_pick_list: list[str] = None,
    self_exclude: bool = None,
    only_active_users: bool = None,
    user_id: str,
    team_id: str,
    channel_id: str,
) -> Response:
    # TODO assert_strategy_is_valid(strategy)
    command = Command.find_one_by_name_and_chanel(command_to_update, channel_id)

    new_values = compute_new_values(
        command,
        command_name=command_to_update,
        label=label,
        strategy=strategy,
        pick_list=pick_list,
        add_to_pick_list=add_to_pick_list,
        remove_from_pick_list=remove_from_pick_list,
        self_exclude=self_exclude,
        only_active_users=only_active_users,
        user_id=user_id,
        team_id=team_id,
        channel_id=channel_id,
    )
    Command.update(command.name, command.channel_id, user_id, new_values)
    updated_command = Command.find_one_by_name_and_chanel(command_to_update, channel_id)

    message_content = f"Command {updated_command.name} successfully updated.\n"
    message_content += format_custom_command_help(updated_command)

    return Response(
        type=SlackResponseType.SLACK_SEND_MESSAGE_IN_CHANNEL.value,
        data={
            "message": Message(
                content=message_content,
                status=MessageStatus.SUCCESS,
                visibility=MessageVisibility.NORMAL,
            )
        },
    )


def compute_new_values(command: Command, **payload: dict[str, any]) -> dict[str, any]:
    new_values = compute_new_values_for_simple_fields(
        ["label", "self_exclude", "only_active_users", "strategy"], **payload
    )

    new_pick_list, new_weight_list = compute_new_pick_list_and_weight_list(
        command, **payload
    )

    new_values["pick_list"] = new_pick_list
    new_values["weight_list"] = new_weight_list

    return new_values


def compute_new_values_for_simple_fields(
    fields_to_look_for_update: list[str], **payload: dict[str, any]
) -> dict[str, any]:
    new_values = {}
    for field in fields_to_look_for_update:
        if payload[field] or payload[field] is False:
            new_values[field] = payload[field]
    return new_values


def compute_new_pick_list_and_weight_list(
    command: Command,
    *,
    strategy: str,
    pick_list: list[str],
    add_to_pick_list: list[str],
    remove_from_pick_list: list[str],
    team_id: str,
    channel_id: str,
    **payload,
) -> tuple[list[str], list[float]]:
    (
        values_to_add_to_pick_list,
        values_to_remove_from_pick_list,
    ) = get_values_to_update(
        command.pick_list,
        new_pick_list=format_pick_list(pick_list, team_id, channel_id)
        if pick_list
        else None,
        items_to_add=add_to_pick_list,
        items_to_remove=remove_from_pick_list,
    )

    indices_of_items_to_remove = get_indices_of_items_to_remove(
        command.pick_list, values_to_remove_from_pick_list
    )
    assert_pick_list_can_be_updated(
        len(command.pick_list),
        len(values_to_add_to_pick_list),
        len(indices_of_items_to_remove),
    )
    new_pick_list = compute_new_pick_list(
        command.pick_list, values_to_add_to_pick_list, indices_of_items_to_remove
    )

    strategy_name = strategy if strategy else command.strategy
    strategy = get_strategy(
        strategy_name,
        command.weight_list if not strategy else None,
        len(new_pick_list),
    )
    new_weight_list = compute_new_weight_list(
        strategy, values_to_add_to_pick_list, indices_of_items_to_remove
    )

    return new_pick_list, new_weight_list
