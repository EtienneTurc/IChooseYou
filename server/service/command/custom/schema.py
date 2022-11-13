from marshmallow import EXCLUDE, Schema, ValidationError, fields, validates

from server.service.validator.command import validate_number_of_items_to_select


class CustomCommandProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    command_name = fields.Str(required=True)
    additional_text = fields.Str(required=False)
    number_of_items_to_select = fields.Int(required=False)
    should_update_command = fields.Bool(required=False)
    with_wheel = fields.Bool(required=False)

    @validates("command_name")
    def valid_command_name(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

    @validates("number_of_items_to_select")
    def valid_number_of_items_to_select(self, number_of_items_to_select) -> None:
        if number_of_items_to_select is not None:
            validate_number_of_items_to_select(number_of_items_to_select)
