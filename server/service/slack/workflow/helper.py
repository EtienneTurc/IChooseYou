from server.service.slack.workflow.enum import OutputVariable


def create_select_item_name(index: int) -> str:
    return f"{OutputVariable.SELECTED_ITEM.value}_{index}"


def create_value_dict(value: any) -> dict[str, any]:
    return {"value": value}
