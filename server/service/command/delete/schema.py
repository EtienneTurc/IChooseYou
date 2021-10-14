from marshmallow import Schema, ValidationError, fields, validates, EXCLUDE


class DeleteCommandProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    channel_id = fields.Str(required=True)
    command_to_delete = fields.Str(required=True)

    @validates("command_to_delete")
    def valid_command_name(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")
