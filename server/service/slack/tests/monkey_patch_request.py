from slack_sdk import WebClient

from server.service.slack.request import get_users_in_channel


def monkey_patch_WebClient():
    return


def monkey_patch_get_users_in_channel(team_id, channel_id):
    return ["1234", "2345", "3456"]


get_users_in_channel.__code__ = monkey_patch_get_users_in_channel.__code__
WebClient.__code__ = monkey_patch_WebClient.__code__