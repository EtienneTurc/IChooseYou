from pymodm import MongoModel, fields

from server.service.error.type.bad_request_error import BadRequestError
from server.service.error.type.missing_element_error import MissingElementError


# Now let's define some Models.
class SlackBotToken(MongoModel):
    team_id = fields.CharField(required=True)
    team_name = fields.CharField(required=True)
    scope = fields.CharField(required=True)
    token_type = fields.CharField(required=True)
    access_token = fields.CharField(required=True)
    bot_user_id = fields.CharField(required=True)

    @staticmethod
    def find_by_team_id(team_id, catch=True):
        if not catch:
            return SlackBotToken.objects.get({"team_id": team_id})

        try:
            return SlackBotToken.objects.get({"team_id": team_id})
        except SlackBotToken.DoesNotExist:
            raise MissingElementError("Slack bot token not found.")

    @staticmethod
    def create(*, team_id, team_name, scope, token_type, access_token, bot_user_id):
        try:
            SlackBotToken.find_by_team_id(team_id, catch=False)
            raise BadRequestError("Slack bot token already exists.")
        except SlackBotToken.DoesNotExist:
            SlackBotToken(
                team_id, team_name, scope, token_type, access_token, bot_user_id
            ).save()
