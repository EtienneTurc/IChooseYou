from scripts.migrations.connection import *  # noqa F401, F403
from server.orm.command import Command
from server.service.strategy.enum import Strategy

commands = Command.objects.raw({"strategy": None})

print(f"UPDATING {commands.count()} COMMANDS !")

for command in commands:
    try:
        Command.update(
            command.name,
            command.channel_id,
            command.updated_by_user_id,
            {
                "strategy": Strategy.uniform.name,
                "weight_list": [1 / len(command.pick_list) for _ in command.pick_list],
            },
        )
    except Exception as err:
        print(err)
