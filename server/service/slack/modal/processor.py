from server.orm.command import Command
from server.service.command.delete.processor import delete_command_processor
from server.service.slack.modal.custom_command_modal import build_custom_command_modal
from server.service.slack.modal.enum import SlackModalSubmitAction
from server.service.slack.modal.instant_command_modal import build_instant_command_modal
from server.service.slack.modal.main_modal import build_main_modal
from server.service.slack.modal.upsert_command_modal import build_upsert_command_modal


def open_main_modal_processor(
    *,
    channel_id: str,
    **kwargs,
) -> dict[str, any]:
    commands = Command.find_all_in_chanel(channel_id)
    modal = build_main_modal(channel_id=channel_id, commands=commands, **kwargs)

    return {"modal": modal}


def build_custom_command_modal_processor(
    *,
    command_name: str,
    channel_id: str,
    additional_text: str = None,
    number_of_items_to_select: int = None,
    with_wheel: bool = False,
    **kwargs,
) -> dict[str, any]:
    command = Command.find_one_by_name_and_chanel(command_name, channel_id)
    modal = build_custom_command_modal(
        command_id=command._id,
        command_name=command.name,
        size_of_pick_list=len(command.pick_list),
        additional_text=additional_text,
        number_of_items_to_select=number_of_items_to_select,
        with_wheel=with_wheel,
    )
    return {"modal": modal}


def build_instant_command_modal_processor(**kwargs) -> dict[str, any]:
    modal = build_instant_command_modal(**kwargs)
    return {"modal": modal}


def build_create_command_modal_processor(
    *,
    channel_id: str = "",
    **kwargs,
) -> dict[str, any]:
    modal = build_upsert_command_modal(False, channel_id=channel_id)
    return {"modal": modal}


def build_update_command_modal_processor(
    *,
    command_id: str,
    **kwargs,
) -> dict[str, any]:
    command = Command.find_by_id(command_id)

    only_users_in_pick_list = command.only_users_in_pick_list
    user_pick_list = command.pick_list if only_users_in_pick_list else None
    free_pick_list = command.pick_list if not only_users_in_pick_list else None

    modal = build_upsert_command_modal(
        True,
        channel_id=command.channel_id,
        command_name=command.name,
        description=command.description,
        label=command.label,
        user_pick_list=user_pick_list,
        free_pick_list=free_pick_list,
        only_users_in_pick_list=command.only_users_in_pick_list,
        strategy=command.strategy,
        self_exclude=command.self_exclude,
        only_active_users=command.only_active_users,
    )
    return {"modal": modal}


def update_upsert_modal_view_processor(
    *,
    callback_id: str,
    channel_id: str,
    new_channel_id: str = None,
    command_to_update: str = None,
    **kwargs,
) -> dict[str, any]:
    if callback_id == SlackModalSubmitAction.UPDATE_COMMAND.value:
        return {
            "modal": build_upsert_command_modal(
                True,
                channel_id=new_channel_id,
                previous_channel_id=channel_id,
                command_name=command_to_update,
                **kwargs,
            )
        }

    return {"modal": build_upsert_command_modal(False, channel_id=channel_id, **kwargs)}


def switch_pick_list_processor(**kwargs):
    return update_upsert_modal_view_processor(**kwargs)


def add_element_to_pick_list_processor(
    *,
    free_pick_list: list[str],
    free_pick_list_item: str,
    free_pick_list_input_block_id: str,  # to reset block
    **kwargs,
):
    if free_pick_list_item is None:
        return update_upsert_modal_view_processor(
            free_pick_list=free_pick_list, **kwargs
        )

    new_pick_list = (free_pick_list or []) + [free_pick_list_item]
    return update_upsert_modal_view_processor(
        free_pick_list=new_pick_list, free_pick_list_item="", **kwargs
    )


def remove_element_from_pick_list_processor(
    *, free_pick_list: list[str], index_item_to_remove: int, **kwargs
):
    new_pick_list = free_pick_list[:]
    del new_pick_list[index_item_to_remove]
    return update_upsert_modal_view_processor(free_pick_list=new_pick_list, **kwargs)


def build_delete_command_processor(
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
