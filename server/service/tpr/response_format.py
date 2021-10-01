from dataclasses import dataclass


@dataclass
class Response:
    type: str
    data: dict[str, any] = {}
