import logging

from flask import current_app


def log_error(
    *,
    error: Exception,
    request: dict[str, any],
    team_id: str,
    channel_id: str,
    user_id: str,
) -> None:
    logging_data = {
        "message": error,
        "route": request.get("route"),
        "method": request.get("method"),
        "team_id": team_id,
        "user_id": user_id,
        "channel_id": channel_id,
    }

    if current_app.config["DEBUG"]:
        logging.exception(logging_data)
    else:
        logging.error(logging_data)
