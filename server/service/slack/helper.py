def is_mention(text: str) -> bool:
    return text and text.startswith("<@") and text.endswith(">")


def get_user_id_in_mention(text: str) -> int:
    text_clean = text[2:-1]
    return text_clean.split("|")[0]


def format_callback_id(callback_action: str, id: int) -> str:
    return f"{callback_action}.{id}"


def get_callback_action(callback_id: str) -> str:
    return callback_id.split(".")[0]


def get_id_from_callback_id(callback_id: str) -> str:
    return callback_id.split(".")[1]
