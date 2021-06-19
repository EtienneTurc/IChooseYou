from slack_sdk import WebClient

from server.service.slack.request import get_users_in_channel, is_user_of_team_active


def monkey_patch_WebClient():
    return


def monkey_patch_get_users_in_channel(team_id: str, channel_id: str) -> list[str]:
    return ["1234", "2345", "3456"]


def monkey_patch_is_user_of_team_active(team_id: str, user_id: str) -> bool:
    print(user_id)
    print()
    return user_id == "1234"


WebClient.__code__ = monkey_patch_WebClient.__code__
get_users_in_channel.__code__ = monkey_patch_get_users_in_channel.__code__
is_user_of_team_active.__code__ = monkey_patch_is_user_of_team_active.__code__
