from enum import Enum


class SlackResponseType(Enum):
    SLACK_SEND_MESSAGE_IN_CHANNEL = "slack_send_message_in_channel"
    SLACK_DELETE_MESSAGE_IN_CHANNEL = "slack_delete_message_in_channel"
    SLACK_SEND_MESSAGE_IN_CHANNEL_VIA_WEBHOOK = (
        "slack_send_message_in_channel_via_webhook"
    )
    SLACK_OPEN_VIEW_MODAL = "slack_open_view_modal"
    SLACK_PUSH_NEW_VIEW_MODAL = "slack_push_new_view_modal"
    SLACK_SAVE_WORKFLOW = "slack_save_workflow"
    SLACK_COMPLETE_WORKFLOW = "slack_complete_workflow"
    SLACK_FAILED_WORKFLOW = "slack_failed_workflow"
