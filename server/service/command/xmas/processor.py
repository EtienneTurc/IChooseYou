import logging

from server.orm.channel import Channel
from server.service.command.xmas.dialogues import (
    xmas_alice_message,
    xmas_christian_message,
    xmas_henry_message,
    xmas_irene_message,
    xmas_marie_message,
    xmas_solenne_message,
    xmas_ulysse_message,
    xmas_xavier_message,
)
from server.service.command.xmas.schema import (
    XmasCelebrationProcessorSchema,
    XmasProcessorSchema,
)
from server.service.slack.message import Message, MessageStatus, MessageVisibility
from server.service.slack.message_formatting import (
    extract_label_from_pick_list,
    format_mention_user,
)
from server.service.validator.decorator import validate_schema
from server.service.wheel.builder import build_wheel

XMAS_CHARACTERS = {
    "Irene": {"male": False, "message": xmas_irene_message()},
    "Christian": {"male": True, "message": xmas_christian_message()},
    "Henry": {"male": True, "message": xmas_henry_message()},
    "Ulysse": {"male": True, "message": xmas_ulysse_message()},
    "Xavier": {"male": True, "message": xmas_xavier_message()},
    "Marie": {"male": False, "message": xmas_marie_message()},
    "Alice": {"male": False, "message": xmas_alice_message()},
    "Solenne": {"male": False, "message": xmas_solenne_message()},
}


CHARACTER_NAMES = XMAS_CHARACTERS.keys()


@validate_schema(XmasCelebrationProcessorSchema)
def xmas_celebration_processor(
    *, user_id: str, team_id: str, **kwargs
) -> dict[str, any]:
    logging.info(f"{format_mention_user(user_id)} found xmas celebration command")
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
def xmas_processor(
    *, additional_text: str, user_id: str, channel_id: str, **kwargs
) -> dict[str, any]:
    print(f"{format_mention_user(user_id)} found xmas command")
    character = additional_text.split(" ")[0]

    if not character:
        return {
            "message": Message(
                content="Slash command expects extra text.",
                visibility=MessageVisibility.HIDDEN,
                status=MessageStatus.ERROR,
            )
        }

    if character not in CHARACTER_NAMES:
        return {
            "message": Message(
                content=f"Character {character} does not exist.",
                visibility=MessageVisibility.HIDDEN,
                status=MessageStatus.ERROR,
            )
        }

    if character == "Solenne":
        extra_text = additional_text.split(" ")[1]
        if not extra_text:
            return {
                "message": Message(
                    content="To chat with Solenne, you will need to pass a key, exemple: `/ichu xmas Solenne 123456789`",  # noqa E501
                    visibility=MessageVisibility.HIDDEN,
                    status=MessageStatus.ERROR,
                )
            }

        if extra_text != "2614214250078801614":
            return {
                "message": Message(
                    content="To chat with Solenne, you will need to enter the correct code.",  # noqa E501
                    visibility=MessageVisibility.HIDDEN,
                    status=MessageStatus.ERROR,
                )
            }
        else:
            print(f"{format_mention_user(user_id)} found easter egg.")
            Channel.upsert(channel_id=channel_id, found_xmas_easter_egg=True)

    message = XMAS_CHARACTERS[character]["message"]

    return {
        "message": Message(
            content=message, visibility=MessageVisibility.NORMAL, as_attachment=False
        )
    }
