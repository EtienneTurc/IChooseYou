from slack_sdk.webhook import WebhookClient

from server.service.slack.message import Message


def send_to_channel(message: Message, response_url: str) -> None:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{message.content}",
            },
        },
    ]

    webhook = WebhookClient(response_url)
    webhook.send(
        text=f"{message.content}" if not message.as_attachment else "",
        response_type=message.visibility.value,
        replace_original=False,
        attachments=[
            {
                "color": message.status.value,
                "blocks": blocks,
            }
        ]
        if message.as_attachment
        else None,
    )
