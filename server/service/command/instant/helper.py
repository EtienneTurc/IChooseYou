from server.service.error.type.consistency_error import ConsistencyError
from server.service.error.type.missing_element_error import MissingElementError


def assert_selected_items(selected_items: list[str], only_active_users: bool) -> None:
    for selected_item in selected_items:
        if selected_item is None:
            if only_active_users:
                message = "No active users to select found."
                raise MissingElementError(message)

            raise ConsistencyError("Could not find an item to select")
