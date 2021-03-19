from slack_sdk import WebClient

from server.orm.slack_bot_token import SlackBotToken


def get_web_client(team_id):
    token = SlackBotToken.find_by_team_id(team_id).access_token
    return WebClient(token=token)


def get_users_in_channel(team_id, channel_id):
    client = get_web_client(team_id)
    result = client.conversations_members(channel=channel_id)
    return result["members"]
