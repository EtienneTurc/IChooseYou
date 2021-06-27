import threading
from typing import Dict

from flask import current_app


def launch_function_in_thread(function, body: Dict[str, any]) -> None:
    thread = threading.Thread(
        target=function,
        args=(current_app._get_current_object(),),
        kwargs=body,
    )
    thread.start()
    if current_app.config["WAIT_FOR_THREAD_BEFORE_RETURN"]:
        thread.join()
