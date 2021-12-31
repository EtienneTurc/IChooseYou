from marshmallow import EXCLUDE, Schema, ValidationError, fields, validates


class InstantCommandProcessorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True)
    team_id = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    label = fields.Str(required=False)
    pick_list = fields.List(fields.Str(required=True), required=True)
    number_of_items_to_select = fields.Int(required=False)
    only_active_users = fields.Bool(required=False)

    @validates("pick_list")
    def valid_pick_list(self, value):
        if not value:
            raise ValidationError("Field may not be empty.")

    @validates("number_of_items_to_select")
    def valid_number_of_items_to_select(self, value):
        if value is not None and value < 1:
            raise ValidationError("Field may be greater or equal to 1.")
