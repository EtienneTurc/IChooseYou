from dataclasses import dataclass
from datetime import datetime

from server.service.slack.message_formatting import extract_label_from_pick_list


def build_pick_list_id_input(block_id):
    return block_id + "_" + str(datetime.timestamp(datetime.now()))


@dataclass
class PickListBlocksFactory:
    actionIds: any
    blockIds: any

    def buld_pick_list_blocks(
        self,
        *,
        team_id: str,
        user_select_enabled: bool,
        free_pick_list_item: str,
        free_pick_list_input_block_id: str,
        pick_list: list[str],
    ):
        return [
            self.build_pick_list_input(
                user_select_enabled,
                free_pick_list_item,
                free_pick_list_input_block_id,
                pick_list=pick_list,
            ),
            self.build_switch_pick_list_type_button(user_select_enabled),
            *self.build_pick_list_elements_display(
                extract_label_from_pick_list(pick_list, team_id=team_id)
            ),
        ]

    def build_switch_pick_list_type_button(
        self, user_select_enabled: bool
    ) -> dict[str, any]:
        text = (
            "Switch select to text input"
            if user_select_enabled
            else "Switch input to user select"
        )

        return {
            "type": "actions",
            "block_id": self.blockIds.USER_SELECT_ENABLED_BLOCK_ID.value,
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": text, "emoji": True},
                    "value": str(user_select_enabled),
                    "action_id": self.actionIds.USER_SELECT_ENABLED_BUTTON.value,  # noqa E501
                }
            ],
        }

    def build_user_pick_list_input(
        self, block_id: str, optional: str
    ) -> dict[str, any]:
        return {
            "type": "input",
            "block_id": block_id,
            "dispatch_action": True,
            "element": {
                "type": "users_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Pick list",
                    "emoji": True,
                },
                "action_id": self.actionIds.USER_PICK_LIST_INPUT.value,
            },
            "label": {
                "type": "plain_text",
                "text": "Add users to the pick list",
                "emoji": True,
            },
            "optional": optional,
        }

    def build_free_pick_list_input(
        self, free_pick_list_item: str, block_id: str, optional
    ) -> dict[str, any]:
        return {
            "type": "input",
            "block_id": block_id,
            "element": {
                "type": "plain_text_input",
                "action_id": self.actionIds.FREE_PICK_LIST_INPUT.value,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Element to add",
                    "emoji": True,
                },
                "initial_value": free_pick_list_item if free_pick_list_item else "",
            },
            "label": {
                "type": "plain_text",
                "text": "Add elements to the pick list",
                "emoji": True,
            },
            "dispatch_action": True,
            "optional": optional,
        }

    def build_pick_list_elements_display(
        self, pick_list: list[str]
    ) -> list[dict[str, any]]:
        if pick_list is None:
            return []

        sections = []
        for i, item in enumerate(pick_list):
            sections.append(
                {
                    "type": "section",
                    "block_id": self.blockIds.REMOVE_FROM_PICK_LIST_BLOCK_ID.value  # noqa E501
                    + f"_{i}",
                    "text": {"type": "mrkdwn", "text": f"● {item}"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": ":x:", "emoji": True},
                        "action_id": self.actionIds.REMOVE_FROM_PICK_LIST_BUTTON.value,  # noqa E501
                    },
                }
            )
        return sections

    def build_pick_list_input(
        self,
        user_select_enabled: bool,
        free_pick_list_item: str,
        free_pick_list_input_block_id: str = None,
        pick_list: list[str] = None,
    ):
        input_optional = pick_list is not None and len(pick_list) != 0
        if user_select_enabled:
            return self.build_user_pick_list_input(
                build_pick_list_id_input(self.blockIds.USER_PICK_LIST_BLOCK_ID.value),
                input_optional,
            )

        return self.build_free_pick_list_input(
            free_pick_list_item,
            free_pick_list_input_block_id
            if free_pick_list_input_block_id
            else build_pick_list_id_input(self.blockIds.FREE_PICK_LIST_BLOCK_ID.value),
            input_optional,
        )
