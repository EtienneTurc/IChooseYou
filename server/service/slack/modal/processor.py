from server.service.command.delete.processor import delete_command_processor
from server.service.slack.modal.upsert_command_modal import build_upsert_command_modal
from server.orm.command import Command
from server.service.slack.modal.custom_command_modal import build_custom_command_modal
from server.service.slack.modal.main_modal import build_main_modal


def open_main_modal_processor(
    *,
    channel_id: str,
    **kwargs,
) -> dict[str, any]:
    commands = Command.find_all_in_chanel(channel_id)
    modal = build_main_modal(channel_id=channel_id, commands=commands, **kwargs)

    return {"modal": modal}


def main_modal_select_command_processor(
    *,
    command_name: str,
    channel_id: str,
    **kwargs,
) -> dict[str, any]:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    modal = build_custom_command_modal(
        command_id=command._id,
        command_name=command.name,
        size_of_pick_list=len(command.pick_list),
    )
    return {"modal": modal}


def main_modal_create_command_processor(
    *,
    channel_id: str = "",
    **kwargs,
) -> dict[str, any]:
    modal = build_upsert_command_modal(False, channel_id=channel_id)
    return {"modal": modal}


def main_modal_update_command_processor(
    *,
    command_id: str,
    **kwargs,
) -> dict[str, any]:
    command = Command.find_by_id(command_id)

    modal = build_upsert_command_modal(
        True,
        channel_id=command.channel_id,
        command_name=command.name,
        description=command.description,
        label=command.label,
        pick_list=command.pick_list,
        strategy=command.strategy,
        self_exclude=command.self_exclude,
        only_active_users=command.only_active_users,
    )
    return {"modal": modal, "channel_id": command.channel_id}


def main_modal_delete_command_processor(
    *,
    command_id: str,
    channel_id: str,
    **kwargs,
) -> dict[str, any]:
    command = Command.find_by_id(command_id)

    return delete_command_processor(
        channel_id=channel_id,
        command_to_delete=command.name,
    )
