from scripts.connection import *  # noqa F401, F403
from server.orm.command import Command

commands = Command.objects.raw({"strategy": None})

print(f"UPDATING {commands.count()} COMMANDS !")

for command in commands:
    try:
        Command.update(
            command.name,
            command.channel_id,
            command.updated_by_user_id,
            {
                "only_users_in_pick_list": True,
            },
        )
    except Exception as err:
        print(err)
