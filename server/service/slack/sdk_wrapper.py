from slack_sdk import WebClient

from server.orm.slack_bot_token import SlackBotToken
from server.service.slack.message import Message, MessageVisibility


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


def delete_message_in_channel(team_id: str, channel_id: str, ts: str) -> None:
    client = get_web_client(team_id)
    client.chat_delete(channel=channel_id, ts=ts)


def send_message_to_channel(
    message: Message,
    channel_id: str,
    team_id: str,
    user_id: str = None,
) -> None:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{message.content}",
            },
        },
    ]

    client = get_web_client(team_id)
    client_func = (
        client.chat_postEphemeral
        if message.visibility == MessageVisibility.HIDDEN
        else client.chat_postMessage
    )
    client_func(
        channel=channel_id,
        text=f"{message.content}" if not message.as_attachment else "",
        user=user_id,
        attachments=[
            {
                "color": message.status.value,
                "blocks": blocks,
            }
        ]
        if message.as_attachment
        else None,
    )
