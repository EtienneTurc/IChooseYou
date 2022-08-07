from server.orm.command import Command
from server.service.command.create.schema import CreateCommandProcessorSchema
from server.service.command.helper import format_pick_list
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import format_new_command_message
from server.service.strategy.enum import Strategy
from server.service.validator.decorator import validate_schema


@validate_schema(CreateCommandProcessorSchema)
def create_command_processor(
    *,
    user_id: str,
    team_id: str,
    channel_id: str,
    new_command_name: str,
    label: str = "",
    description: str = "",
    pick_list: list[str],
    strategy: str = Strategy.uniform.name,
    self_exclude: bool = False,
    only_active_users: bool = False,
) -> dict[str, any]:
    pick_list = format_pick_list(pick_list, team_id, channel_id)

    strategy_enum = Strategy[strategy]
    weight_list = strategy_enum.value.create_weight_list(len(pick_list))

    Command.create(
        name=new_command_name,
        channel_id=channel_id,
        label=label,
        description=description,
        pick_list=pick_list,
        self_exclude=self_exclude,
        only_active_users=only_active_users,
        weight_list=weight_list,
        strategy=strategy_enum.name,
        created_by_user_id=user_id,
    )
    created_command = Command.find_one_by_name_and_chanel(new_command_name, channel_id)

    message_content = format_new_command_message(
        command_name=created_command.name,
        team_id=team_id,
        pick_list=created_command.pick_list,
        command_description=created_command.description,
        current_user_id=user_id,
    )

    return {
        "message": Message(
            content=message_content,
            status=MessageStatus.SUCCESS,
            visibility=MessageVisibility.NORMAL,
        )
    }
