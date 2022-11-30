from server.service.command.xmas.schema import (XmasCelebrationProcessorSchema,
                                                XmasProcessorSchema)
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import (extract_label_from_pick_list,
                                                     format_mention_user)
from server.service.validator.decorator import validate_schema
from server.service.wheel.builder import build_wheel

XMAS_CHARACTERS = {
    "Irene": {"male": False},
    "Christian": {"male": True},
    "Henry": {"male": True},
    "Ulysse": {"male": True},
    "Xavier": {"male": True},
    "Marie": {"male": False},
    "Alice": {"male": False},
    "Solenne": {"male": False},
}


CHARACTER_NAMES = XMAS_CHARACTERS.keys()


@validate_schema(XmasCelebrationProcessorSchema)
def xmas_celebration_processor(
    *, user_id: str, team_id: str, **kwargs
) -> dict[str, any]:
    print(f"{format_mention_user(user_id)} found xmas celebration command")
    message = f":santa: Ho ho ho ! {format_mention_user(user_id)} did you really think"
    message += " that finding the Christmas easter egg would be that simple ?!"
    message += "\nFortunately for you, the Christmas spirit is all about:"
    message += " _pleasure to give :gift:, joy to receive :open_hands:_."
    message += " So I will give you that: there is a real Christmas easter egg"
    message += " and you already have every clue."
    message += "\n*NB*: Do not delete this message."
    message += " It is funnier to find it out as a team :wink:"

    [user_label] = extract_label_from_pick_list(
        [format_mention_user(user_id)], team_id=team_id
    )
    labels = [*CHARACTER_NAMES, user_label]
    gif_frames = build_wheel(
        [1 / len(labels)] * len(labels),
        labels,
        labels[-1],
    )

    return {
        "message": Message(
            content=message,
            visibility=MessageVisibility.NORMAL,
            as_attachment=False,
        ),
        "selected_items": [user_id],
        "gif_frames": gif_frames,
        "with_wheel": True,
    }


@validate_schema(XmasProcessorSchema)
def xmas_processor(*, additional_text: str, user_id: str, **kwargs) -> dict[str, any]:
    print(f"{format_mention_user(user_id)} found xmas command")
    character = additional_text

    if not character:
        return {
            "message": Message(
                content="Slash command expect extra text.",
                visibility=MessageVisibility.HIDDEN,
                status=MessageStatus.ERROR,
            )
        }

    if character not in CHARACTER_NAMES:
        return {
            "message": Message(
                content=f"Character {character} does not exist.",
                visibility=MessageVisibility.HIDDEN,
            )
        }

    print(f"{format_mention_user(user_id)} found all of xmas 1st part content")
    character_pronoun = "He" if XMAS_CHARACTERS[character]["male"] else "She"

    message = "Well done ! You successfully unraveled the mystery around the first part of the christmas easter egg."  # noqa E501
    message += f" Unfortunately {character} can't answer your call right now."
    message += f" {character_pronoun} will return on the 12th of December."

    return {
        "message": Message(
            content=message,
            visibility=MessageVisibility.HIDDEN,
        )
    }
