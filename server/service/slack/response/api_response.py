from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient

from server.service.slack.message import Message, MessageVisibility
from server.service.slack.response.helper import build_message_payload
from server.service.slack.sdk_helper import (create_slack_sdk_web_client,
                                             create_slack_sdk_webhook_client)


@create_slack_sdk_web_client
def send_message_to_channel(
    client: WebClient,
    *,
    message: Message,
    channel_id: str,
    user_id: str = None,
    thread_ts: str = None,
    team_id: str,
    **kwargs
) -> None:
    payload = build_message_payload(message)
    client_func = (
        client.chat_postEphemeral
        if message.visibility == MessageVisibility.HIDDEN
        else client.chat_postMessage
    )
    return client_func(**payload, channel=channel_id, user=user_id, thread_ts=thread_ts)


@create_slack_sdk_web_client
def send_built_message_to_channel(
    client: WebClient,
    *,
    payload: dict[str, any],
    visibility: MessageVisibility,
    channel_id: str,
    user_id: str = None,
    thread_ts: str = None,
    team_id: str,
    **kwargs
) -> None:
    client_func = (
        client.chat_postEphemeral
        if visibility == MessageVisibility.HIDDEN
        else client.chat_postMessage
    )
    return client_func(**payload, channel=channel_id, user=user_id, thread_ts=thread_ts)


@create_slack_sdk_web_client
def send_file_to_channel(
    client: WebhookClient, *, channel_id: str, file_pointer, team_id: str, **kwargs
) -> None:
    return client.files_upload(
        channels=channel_id,
        file=file_pointer,
    )


@create_slack_sdk_web_client
def delete_message_in_channel(
    client: WebClient, *, channel_id: str, ts: str, team_id: str, **kwargs
) -> None:
    client.chat_delete(channel=channel_id, ts=ts)


@create_slack_sdk_webhook_client
def send_message_to_channel_via_response_url(
    client: WebhookClient, *, message: Message, response_url: str, **kwargs
) -> None:
    payload = build_message_payload(message)
    client.send(
        **payload,
        response_type=message.visibility.value,
        replace_original=False,
    )


@create_slack_sdk_web_client
def open_view_modal(
    client: WebClient, *, modal: str, trigger_id: str, team_id: str, **kwargs
) -> None:
    client.views_open(trigger_id=trigger_id, view=modal)


@create_slack_sdk_web_client
def push_view_modal(
    client: WebClient, *, modal: str, trigger_id: str, team_id: str, **kwargs
) -> None:
    client.views_push(trigger_id=trigger_id, view=modal)


@create_slack_sdk_web_client
def save_workflow(
    client: WebClient,
    *,
    inputs: dict,
    outputs: list[dict],
    workflow_step_edit_id: str,
    team_id: str,
    **kwargs
) -> None:
    client.workflows_updateStep(
        workflow_step_edit_id=workflow_step_edit_id, inputs=inputs, outputs=outputs
    )


@create_slack_sdk_web_client
def complete_workflow(
    client: WebClient,
    *,
    workflow_step_execute_id: str,
    outputs: dict,
    team_id: str,
    **kwargs
):
    client.workflows_stepCompleted(
        workflow_step_execute_id=workflow_step_execute_id, outputs=outputs
    )


@create_slack_sdk_web_client
def failed_worklow(
    client: WebClient,
    *,
    message: str,
    workflow_step_execute_id: str,
    team_id: str,
    **kwargs
):
    error = {"message": message}
    client.workflows_stepFailed(
        workflow_step_execute_id=workflow_step_execute_id, error=error
    )
