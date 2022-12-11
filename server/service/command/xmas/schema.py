from marshmallow import EXCLUDE, Schema, fields


class XmasCelebrationProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)


class XmasProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    additional_text = fields.Str(required=True)
    user_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
