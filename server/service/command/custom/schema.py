from marshmallow import EXCLUDE, Schema, ValidationError, fields, validates


class CustomCommandProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    command_name = fields.Str(required=True)
    additional_text = fields.Str(required=False)
    number_of_items_to_select = fields.Int(required=False)
    should_update_weight_list = fields.Bool(required=False)

    @validates("command_name")
    def valid_command_name(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

    @validates("number_of_items_to_select")
    def valid_number_of_items_to_select(self, value):
        if value is not None and value < 1:
            raise ValidationError("Field may be greater or equal to 1.")
