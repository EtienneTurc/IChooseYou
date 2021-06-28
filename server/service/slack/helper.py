def is_mention(text: str) -> bool:
    return text and text.startswith("<@") and text.endswith(">")


def get_user_id_in_mention(text: str) -> int:
    text_clean = text[2:-1]
    return text_clean.split("|")[0]
