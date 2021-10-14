from dataclasses import dataclass


@dataclass
class DataFlow:
    formatter: any
    processor: any
    responder: any
    error_handler: any
    fast_responder: any = None
