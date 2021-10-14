from marshmallow import Schema, ValidationError, fields, validates, EXCLUDE

from server.service.command.helper import assert_strategy_is_valid


class CreateCommandProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    new_command_name = fields.Str(required=True)
    label = fields.Str(required=False)
    description = fields.Str(required=False)
    pick_list = fields.List(fields.Str(required=True), required=True)
    strategy = fields.Str(required=False)
    self_exclude = fields.Bool(required=False)
    only_active_users = fields.Bool(required=False)

    @validates("new_command_name")
    def valid_command_name(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

        if len(value.split(" ")) > 1:
            raise ValidationError(
                "Command name must be a single word, i.e without spaces."
            )

    @validates("pick_list")
    def valid_pick_list(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

    @validates("strategy")
    def valid_strategy(self, value):
        assert_strategy_is_valid(value)
