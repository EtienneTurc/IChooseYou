from flask import current_app
from marshmallow import Schema, ValidationError, fields, validates


class SlackEntitySchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)


class SlackApiSchema(Schema):
    team_id = fields.Str(required=True)
    channel = fields.Nested(SlackEntitySchema())
    user = fields.Nested(SlackEntitySchema())
    command_name = fields.Str(required=True)
    text = fields.Str(required=True)
    response_url = fields.Str(required=True)

    @validates("command_name")
    def not_empty(self, value):
        if not value:
            raise ValidationError(
                "No command found. Try using "
                + f'`{current_app.config["SLASH_COMMAND"]} help` to get some help.'
            )
