from server.orm.command import Command
from server.service.command.args import Arg
from server.service.command.base_command import BaseCommand, addHelp
from server.service.command.option_cleaning import format_pick_list
from server.service.command.update_helper import (compute_new_pick_list,
                                                  compute_new_weight_list,
                                                  get_indices_of_elements_to_remove,
                                                  get_values_to_update)
from server.service.command.validator import (assert_pick_list_can_be_updated,
                                              assert_strategy_is_valid)
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import format_custom_command_help
from server.service.strategy.helper import get_strategy


class UpdateCommand(BaseCommand):
    def __init__(self, *, text: str, team_id: str, channel_id: str):
        name = "update"
        description = "Update a given command"
        examples = [
            "mySuperCommand --add-to-pick-list my_element_to_add",
            "mySuperCommand --pick-list my new pick list",
            "mySuperCommand --self-exclude --only-active-users",
        ]
        args = [
            Arg(
                name="command_name",
                prefix="",
                nargs=1,
                help="Name of the command to update.",
            ),
            Arg(name="label", short="l", nargs="*", help="New label"),
            Arg(
                name="pick-list",
                short="p",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="New pick list",
            ),
            Arg(
                name="add-to-pick-list",
                short="a",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="Elements to add to the pick list.",
            ),
            Arg(
                name="remove-from-pick-list",
                short="r",
                nargs="*",
                type=list,
                clean_mentions=True,
                help="Elements to remove from the pick list.",
            ),
            Arg(
                name="strategy",
                short="s",
                nargs="*",
                help="Name of the strategy to use.",
            ),
            Arg(
                name="self-exclude",
                short="e",
                nargs="?",
                const="True",
                type=bool,
                help="Exclude the person using the slash command to be picked.",
            ),
            Arg(
                name="only-active-users",
                short="o",
                nargs="?",
                const="True",
                type=bool,
                help="Exclude non active users to be picked.",
            ),
        ]
        super(UpdateCommand, self).__init__(
            text,
            name=name,
            channel_id=channel_id,
            team_id=team_id,
            description=description,
            examples=examples,
            args=args,
        )

    @addHelp
    def exec(self, user_id: str, *args, **kwargs) -> Message:
        assert_strategy_is_valid(self.options["strategy"])

        command_name = self.options["command_name"]
        command = Command.find_one_by_name_and_chanel(command_name, self.channel_id)

        new_values = self._compute_new_values(command)
        Command.update(command.name, command.channel_id, user_id, new_values)
        updated_command = Command.find_one_by_name_and_chanel(
            command_name, self.channel_id
        )

        message_content = f"Command {updated_command.name} successfully updated.\n"
        message_content += format_custom_command_help(updated_command)
        return Message(
            content=message_content,
            status=MessageStatus.SUCCESS,
            visibility=MessageVisibility.NORMAL,
        )

    def _compute_new_values(self, command: Command) -> dict[str, any]:
        new_values = self._compute_new_values_for_simple_fields(
            ["label", "self_exclude", "only_active_users", "strategy"]
        )

        new_pick_list, new_weight_list = self._compute_new_pick_list_and_weight_list(
            command
        )

        new_values["pick_list"] = new_pick_list
        new_values["weight_list"] = new_weight_list

        return new_values

    def _compute_new_values_for_simple_fields(
        self, fields_to_look_for_update: list[str]
    ) -> dict[str, any]:
        new_values = {}
        for field in fields_to_look_for_update:
            if self.options[field] or self.options[field] is False:
                new_values[field] = self.options[field]
        return new_values

    def _compute_new_pick_list_and_weight_list(
        self, command: BaseCommand
    ) -> tuple[list[str], list[float]]:
        (
            values_to_add_to_pick_list,
            values_to_remove_from_pick_list,
        ) = get_values_to_update(
            command.pick_list,
            new_pick_list=format_pick_list(
                self.options["pick_list"], self.team_id, self.channel_id
            )
            if self.options["pick_list"]
            else None,
            elements_to_add=self.options["add_to_pick_list"],
            elements_to_remove=self.options["remove_from_pick_list"],
        )

        indices_of_elements_to_remove = get_indices_of_elements_to_remove(
            command.pick_list, values_to_remove_from_pick_list
        )
        assert_pick_list_can_be_updated(
            len(command.pick_list),
            len(values_to_add_to_pick_list),
            len(indices_of_elements_to_remove),
        )
        new_pick_list = compute_new_pick_list(
            command.pick_list, values_to_add_to_pick_list, indices_of_elements_to_remove
        )

        strategy_name = (
            self.options["strategy"] if self.options["strategy"] else command.strategy
        )
        strategy = get_strategy(
            strategy_name,
            command.weight_list if not self.options["strategy"] else None,
            len(new_pick_list),
        )
        new_weight_list = compute_new_weight_list(
            strategy, values_to_add_to_pick_list, indices_of_elements_to_remove
        )

        return new_pick_list, new_weight_list
