from server.service.slack.interactivity.helper import assert_message_can_be_delete


def delete_message_processor(
    *, user_id: str, message_text: str, **kwargs
) -> dict[str, any]:
    assert_message_can_be_delete(message_text, user_id)
    return {}
