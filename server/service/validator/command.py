from marshmallow import ValidationError

MAX_MULTIPLE_SELECTIONS = 50


def validate_number_of_items_to_select(number_of_items_to_select: int) -> None:
    if number_of_items_to_select < 1:
        raise ValidationError("Must select at least 1 item.")

    if number_of_items_to_select > MAX_MULTIPLE_SELECTIONS:
        raise ValidationError(
            f"Selecting more than {MAX_MULTIPLE_SELECTIONS} at once is prohibited."
        )
