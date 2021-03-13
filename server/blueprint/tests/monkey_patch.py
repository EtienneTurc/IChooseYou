from slack_sdk.webhook import WebhookClient

from server.slack.utils import slack_signature_valid


def monkey_patch_webhook_send(
    self,
    *,
    text=None,
    attachments=None,
    blocks=None,
    response_type=None,
    replace_original=None,
    delete_original=None,
    headers=None,
):
    print(attachments)


WebhookClient.send.__code__ = monkey_patch_webhook_send.__code__

slack_signature_valid.__code__ = (lambda x: True).__code__
