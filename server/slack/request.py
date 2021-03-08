import os

from slack_sdk import WebClient

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def get_users_in_channel(channel_id):
    result = client.conversations_members(channel=channel_id)
    return result["members"]
