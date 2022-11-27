from server.service.slack.message_formatting import format_mention_user


def is_a_xmas_message(text: str):
    return text.startswith(":santa:")


def format_christmas_delete_message(user_id: str):
    message = f":santa: Ho ho ho ! {format_mention_user(user_id)}"
    message += " did not want to share the easter egg information"
    message += " with everyone else. That's not the Christmas spirit."
    message += " For instance bringing croissants would"
    message += " fit the spirit :trollface:."
    message += "\nI told you, it is not that easy :wink:."
    return message
