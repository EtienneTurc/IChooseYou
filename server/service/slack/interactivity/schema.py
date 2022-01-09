from marshmallow import EXCLUDE, Schema, fields


class DeleteMessageProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    ts = fields.Str(required=True)
    message_text = fields.Str(required=True)
