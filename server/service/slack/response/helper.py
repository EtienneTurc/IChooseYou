from server.service.slack.message import Message


def build_message_payload(message: Message):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{message.content}",
            },
        }
    ]

    if message.image_url:
        blocks.append(
            {"type": "image", "image_url": message.image_url, "alt_text": "dsfdsf"}
        )

    return {
        "text": f"{message.content}" if not message.as_attachment else "",
        "attachments": [
            {
                "color": message.status.value,
                "blocks": blocks,
            }
        ]
        if message.as_attachment
        else None,
    }
