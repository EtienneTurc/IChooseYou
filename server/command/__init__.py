from server.command.create import CreateCommand
from server.command.custom import CustomCommand

KNOWN_COMMANDS = ["create"]

__all__ = ["CreateCommand", "CustomCommand", "KNOWN_COMMANDS"]
