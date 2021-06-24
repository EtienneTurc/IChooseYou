from dataclasses import dataclass
from enum import Enum


class MessageStatus(Enum):
    INFO = "#3498db"
    SUCCESS = "#2ecc71"
    LIGHT_ERROR = "#e74c3c"
    ERROR = "#c0392b"


class MessageVisibility(Enum):
    HIDDEN = "ephemeral"
    NORMAL = "in_channel"


@dataclass
class Message:
    content: str
    status: MessageStatus = MessageStatus.INFO
    visibility: MessageVisibility = MessageVisibility.HIDDEN
    as_attachment: bool = True
    image_url: str = None
