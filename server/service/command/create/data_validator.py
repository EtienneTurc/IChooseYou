# from dataclasses import dataclass

# def build_required_message(payload_field: str) -> str:
#     return f"{payload_field} is required."

# pick_list_message= ""

# @dataclass
# class ValidationConfig:
#     error_condition: any
#     message: str


# VALIDATION_ERROR_MESSAGE = {
#     "command_name": build_required_message("Command name"),
#     "label": build_required_message("Command name"),
#     "label": build_required_message("Command name"),
# }


# def validate_payload(func, ):
#     def validate_payload_wrapper(*args, **kwargs):
#         for key in

#         if not kwargs.get("command_name"):
#             raise Exception("Command name is required.")

#         return func(*args, **kwargs)

#     return validate_payload_wrapper


# command_name: str,
#     label: str,
#     pick_list: list[str],
#     strategy_name: str,
#     self_exclude: bool,
#     only_active_users: bool,
#     user_id: str,
#     team_id: str,
#     channel_id: str,
