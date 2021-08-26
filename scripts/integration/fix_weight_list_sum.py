import numpy as np

from scripts.connection import *  # noqa F401, F403
from server.orm.command import Command

commands = Command.objects.raw({})

print(f"RECOVERING DATA {commands.count()} COMMANDS !")

for command in commands:
    weight_list = command.weight_list
    print(np.sum(weight_list))
    try:
        if weight_list and np.sum(weight_list) != 1:
            Command.update(
                command.name,
                command.channel_id,
                command.updated_by_user_id,
                {
                    "weight_list": list(np.array(weight_list) / np.sum(weight_list)),
                },
            )
    except Exception as err:
        print(err)
