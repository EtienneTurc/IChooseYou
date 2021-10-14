from server.service.error.type.bad_request_error import BadRequestError


def assert_message_can_be_delete(text: str, user_id: str) -> bool:
    text_split = text.split("Hey ! <@")
    if len(text_split) <= 1:
        raise BadRequestError("Only pick messages can be deleted.")

    user_id_size = len(user_id)
    expected_user_id = text_split[1][:user_id_size]

    if expected_user_id != user_id:
        message = "Only the user that triggered the slash command can delete"
        message += " the corresponding message."
        raise BadRequestError(message)
