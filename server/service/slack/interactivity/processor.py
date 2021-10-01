from server.service.tpr.response_format import Response
from server.service.slack.response.response_type import SlackResponseType
from server.service.slack.interactivity.helper import assert_message_can_be_delete


def delete_message_processor(*, user_id: str, message_text: str, **kwargs) -> Response:
    assert_message_can_be_delete(message_text, user_id)
    return Response(type=SlackResponseType.SLACK_DELETE_MESSAGE_IN_CHANNEL.value)
