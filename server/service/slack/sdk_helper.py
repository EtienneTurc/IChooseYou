from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient

from server.orm.slack_bot_token import SlackBotToken


def get_web_client(team_id: str) -> WebClient:
    token = SlackBotToken.find_by_team_id(team_id).access_token
    return WebClient(token=token)


def create_slack_sdk_web_client(func):
    def create_slack_sdk_client_wrapper(*args, **kwargs):
        client = get_web_client(kwargs.get("team_id"))
        return func(client, *args, **kwargs)

    return create_slack_sdk_client_wrapper


def create_slack_sdk_webhook_client(func):
    def create_slack_sdk_client_wrapper(*args, **kwargs):
        client = WebhookClient(kwargs.get("response_url"))
        return func(client, *args, **kwargs)

    return create_slack_sdk_client_wrapper


@create_slack_sdk_web_client
def get_users_in_channel(
    client: WebClient, *, channel_id: str, team_id: str, **kwargs
) -> list[str]:
    result = client.conversations_members(channel=channel_id)
    return result["members"]


@create_slack_sdk_web_client
def is_user_of_team_active(
    client: WebClient, *, user_id: str, team_id: str, **kwargs
) -> bool:
    result = client.users_getPresence(user=user_id)
    return result["presence"] == "active"
