from marshmallow import EXCLUDE, Schema, ValidationError, fields, validates

from server.service.validator.command import validate_number_of_items_to_select


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
    def valid_number_of_items_to_select(self, number_of_items_to_select: int) -> None:
        if number_of_items_to_select is not None:
            validate_number_of_items_to_select(number_of_items_to_select)
