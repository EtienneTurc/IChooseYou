import pytest

from server.service.error.logger import log_error
from server.tests.test_app import *  # noqa: F401, F403

exception_1 = Exception("Exception 1")
exception_2 = Exception("Exception 2")


@pytest.mark.parametrize(
    "error, req, team_id, channel_id, user_id, expected_text",
    [
        (exception_1, {}, None, None, None, "ERROR"),
        (exception_1, {}, None, None, None, "root:logger.py"),
        (exception_1, {}, None, None, None, "'message': Exception('Exception 1')"),
        (exception_2, {}, None, None, None, "'message': Exception('Exception 2')"),
        (exception_2, {"route": "/my/route"}, None, None, None, "'route': '/my/route'"),
        (exception_2, {"method": "GET"}, None, None, None, "'method': 'GET'"),
        (exception_2, {}, 1234, None, None, "'team_id': 1234"),
        (exception_2, {}, None, 2345, None, "'channel_id': 2345"),
        (exception_2, {}, None, None, 3456, "'user_id': 3456"),
    ],
)
def test_slash_command_create(
    error, req, team_id, channel_id, user_id, expected_text, caplog, client
):
    log_error(
        error=error,
        request=req,
        team_id=team_id,
        channel_id=channel_id,
        user_id=user_id,
    )
    assert expected_text in caplog.text
