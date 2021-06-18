import os

from slack_sdk import WebClient

from server.orm.slack_bot_token import SlackBotToken

client_id = os.environ.get("SLACK_CLIENT_ID")
client_secret = os.environ.get("SLACK_CLIENT_SECRET")


def register(code):
    client = WebClient()

    try:
        response = client.oauth_v2_access(
            client_id=client_id, client_secret=client_secret, code=code
        )

        SlackBotToken.create(
            team_id=response["team"]["id"],
            team_name=response["team"]["name"],
            scope=response["scope"],
            token_type=response["token_type"],
            access_token=response["access_token"],
            bot_user_id=response["bot_user_id"],
        )
    except Exception as e:
        return str(e)

    return "I choose you successfully installed!"
