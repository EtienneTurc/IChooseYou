from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient

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


def send_message_to_channel(
    message: Message,
    channel_id: str,
    team_id: str,
    user_id: str = None,
) -> None:
    payload = build_message_payload(message)
    client = get_web_client(team_id)
    client_func = (
        client.chat_postEphemeral
        if message.visibility == MessageVisibility.HIDDEN
        else client.chat_postMessage
    )
    client_func(
        **payload,
        channel=channel_id,
        user=user_id,
    )


def send_message_to_channel_via_response_url(
    message: Message, response_url: str
) -> None:
    payload = build_message_payload(message)
    webhook = WebhookClient(response_url)
    webhook.send(
        **payload,
        response_type=message.visibility.value,
        replace_original=False,
    )


def open_view_modal(modal: str, trigger_id: str, team_id: str) -> None:
    client = get_web_client(team_id)
    client.views_open(trigger_id=trigger_id, view=modal)


def save_workflow_in_slack(
    inputs: dict, outputs: list[dict], workflow_step_edit_id: str, team_id: str
) -> None:
    client = get_web_client(team_id)
    client.workflows_updateStep(
        workflow_step_edit_id=workflow_step_edit_id, inputs=inputs, outputs=outputs
    )


def complete_workflow(workflow_step_execute_id: str, outputs: dict, team_id: str):
    client = get_web_client(team_id)
    client.workflows_stepCompleted(
        workflow_step_execute_id=workflow_step_execute_id, outputs=outputs
    )


def failed_worklow(message: str, workflow_step_execute_id: str, team_id: str):
    client = get_web_client(team_id)
    error = {"message": message}
    client.workflows_stepFailed(
        workflow_step_execute_id=workflow_step_execute_id, error=error
    )
