from server.service.error.back_error import BackError


ERROR_TO_RESPONSE_ACTION = {BackError: lambda: print("in response action")}
