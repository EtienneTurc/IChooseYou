from marshmallow import EXCLUDE, Schema, ValidationError, fields, validates

from server.blueprint.slash_command.action import KNOWN_SLASH_COMMANDS_ACTIONS
from server.service.command.helper import assert_strategy_is_valid
from server.service.helper.list_helper import format_list_to_string


class UpdateCommandProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    command_to_update = fields.Str(required=True)
    new_channel_id = fields.Str(required=False)
    new_command_name = fields.Str(required=False)
    label = fields.Str(required=False)
    description = fields.Str(required=False)
    pick_list = fields.List(fields.Str(required=False))
    add_to_pick_list = fields.List(fields.Str(required=False))
    remove_from_pick_list = fields.List(fields.Str(required=False))
    strategy = fields.Str(required=False)
    self_exclude = fields.Bool(required=False)
    only_active_users = fields.Bool(required=False)

    @validates("command_to_update")
    def valid_command_name(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

    @validates("new_command_name")
    def valid_new_command_name(self, value):
        if value in KNOWN_SLASH_COMMANDS_ACTIONS:
            raise ValidationError(
                f"Command name can not be one of these: {format_list_to_string(KNOWN_SLASH_COMMANDS_ACTIONS)}"  # noqa E501
            )

    @validates("pick_list")
    def valid_pick_list(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

    @validates("strategy")
    def valid_strategy(self, value):
        assert_strategy_is_valid(value)
