from slack_sdk import WebClient
from slack_sdk.webhook.client import WebhookClient

from server.service.slack.decorator import is_signature_valid
from server.service.slack.modal.pick_list_blocks import build_pick_list_id_input
from server.service.slack.responder.message import wait_for_wheel_to_finish
from server.service.slack.sdk_helper import get_web_client


def monkey_patch_get_web_client(team_id: str) -> WebClient:
    return WebClient(token="1234")


def monkey_patch_client_conversations_members(self, *args, **kwargs):
    return {"members": ["1234", "2345", "3456"]}


def monkey_patch_client_users_info(self, *, user: str, **kwargs):
    return {"user": {"profile": {"display_name": user}}}


def monkey_patch_client_users_getPresence(self, *, user: str, **kwargs):
    return {"presence": "active" if user == "1234" else "away"}


def monkey_patch_client_chat_delete(self, **kwargs):
    return {"status": 200}


def monkey_patch_client_chat_postEphemeral(
    self, *, channel: str, user: str, text: str, attachments: str, **kwargs
):
    print(text)
    print(attachments)


def monkey_patch_client_chat_postMessage(
    self, *, channel: str, user: str, text: str, attachments: str, **kwargs
):
    print(text)
    print(attachments)


def monkey_patch_views_open(self, *, trigger_id: str, view: str, **kwargs):
    print(trigger_id)
    print(view)


def monkey_patch_webhook_client_send(self, *, text: str, attachments: str, **kwargs):
    print(text)
    print(attachments)


def monkey_patch_workflows_updateStep(
    self, *, workflow_step_edit_id: str, inputs: dict, outputs: list[dict], **kwargs
):
    print(inputs)
    print(outputs)


def monkey_patch_workflows_stepCompleted(self, *, workflow_step_execute_id, outputs):
    print(outputs)


def monkey_patch_workflows_stepFailed(
    self, *, workflow_step_execute_id, error, **kwargs
):
    print(error)


def monkey_patch_files_upload(self, *, file: str, channels, **kwargs):
    print(f"File {file} uploaded")

    from dataclasses import dataclass

    @dataclass
    class Data:
        data: any

    return Data(data={"file": {"shares": {"public": {channels: [{"ts": "1234"}]}}}})


def monkey_patch_views_push(self, *, view: str, **kwargs):
    print(view)


def monkey_patch_views_update(self, *, view: str, **kwargs):
    print(view)


def monkey_patch_build_pick_list_id_input(block_id):
    return block_id


def monkey_patch_sleep():
    pass


get_web_client.__code__ = monkey_patch_get_web_client.__code__

WebClient.conversations_members.__code__ = (
    monkey_patch_client_conversations_members.__code__
)
WebClient.users_info.__code__ = monkey_patch_client_users_info.__code__
WebClient.users_getPresence.__code__ = monkey_patch_client_users_getPresence.__code__
WebClient.chat_delete.__code__ = monkey_patch_client_chat_delete.__code__
WebClient.chat_postEphemeral.__code__ = monkey_patch_client_chat_postEphemeral.__code__
WebClient.chat_postMessage.__code__ = monkey_patch_client_chat_postMessage.__code__
WebClient.views_open.__code__ = monkey_patch_views_open.__code__
WebClient.workflows_updateStep.__code__ = monkey_patch_workflows_updateStep.__code__
WebClient.workflows_stepCompleted.__code__ = (
    monkey_patch_workflows_stepCompleted.__code__
)
WebClient.workflows_stepFailed.__code__ = monkey_patch_workflows_stepFailed.__code__
WebClient.files_upload.__code__ = monkey_patch_files_upload.__code__
WebClient.views_push.__code__ = monkey_patch_views_push.__code__
WebClient.views_update.__code__ = monkey_patch_views_update.__code__

WebhookClient.send.__code__ = monkey_patch_webhook_client_send.__code__

is_signature_valid.__code__ = (lambda x: True).__code__
build_pick_list_id_input.__code__ = monkey_patch_build_pick_list_id_input.__code__
wait_for_wheel_to_finish.__code__ = monkey_patch_sleep.__code__
