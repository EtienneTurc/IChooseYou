from slack_sdk import WebClient

from server.orm.slack_bot_token import SlackBotToken


def get_web_client(team_id: str) -> WebClient:
    token = SlackBotToken.find_by_team_id(team_id).access_token
    return WebClient(token=token)


def get_users_in_channel(team_id: str, channel_id: str) -> list[str]:
    client = get_web_client(team_id)
    result = client.conversations_members(channel=channel_id)
    return result["members"]


def is_user_of_team_active(team_id: str, user_id: str) -> bool:
    client = get_web_client(team_id)
    result = client.users_getPresence(user=user_id)
    return result["presence"] == "active"
