import random
from dataclasses import dataclass

from server.service.helper.dict_helper import normalize
from server.service.slack.helper import get_user_id_in_mention, is_mention
from server.service.slack.sdk_helper import is_user_of_team_active
from server.service.strategy.assertion import (
    assert_pick_list_has_same_size_than_weight_list, assert_pick_list_is_not_empty,
    assert_pick_list_valid_after_filtering_inactive_users,
    assert_pick_list_valid_after_self_exclusion, assert_weight_list_is_not_empty,
    assert_weight_list_must_sum_up_to_1)


@dataclass
class BaseStrategy:
    pick_list: list[str]
    weight_list: list[float]

    @staticmethod
    def create_weight_list(size: int) -> list[float]:
        return [1 / size for _ in range(size)]

    def __post_init__(self) -> None:
        self.pick_list = self.pick_list[:]
        self.weight_list = self.weight_list[:]

        self.filtered_pick_list = self.pick_list[:]
        self.filtered_weight_list = self.weight_list[:]

        assert_pick_list_is_not_empty(self.pick_list)
        assert_weight_list_is_not_empty(self.weight_list)
        assert_pick_list_has_same_size_than_weight_list(
            self.pick_list, self.weight_list
        )
        assert_weight_list_must_sum_up_to_1(self.weight_list)

    # -------------------------------------------------------------------------
    # ----------------------------- SELECTION ---------------------------------
    # -------------------------------------------------------------------------

    def select(
        self,
        *,
        number_of_items_to_select: int,
        self_exclude: bool = False,
        user_id: str = None,
        only_active_users: bool = False,
        team_id: str = None
    ) -> list[str]:
        if self_exclude and user_id:
            self.exclude_user_from_pick_list(user_id=user_id)
            self._assert_pick_list_valid_after_self_exclusion()

        if only_active_users and team_id:
            self.remove_inactive_users_from_pick_list(team_id=team_id)
            self._assert_pick_list_valid_after_filtering_inactive_users()

        self.filtered_pick_list = self.pick_list[:]
        self.filtered_weight_list = self.weight_list[:]

        return self.select_from_pick_list(
            number_of_items_to_select=number_of_items_to_select
        )

    def exclude_user_from_pick_list(self, *, user_id: str) -> None:
        indices_of_items_to_remove = [
            index for index, item in enumerate(self.pick_list) if user_id in item
        ]
        self.remove_items(indices_of_items_to_remove)

    def remove_inactive_users_from_pick_list(self, *, team_id: str) -> None:
        indices_of_items_to_remove = [
            index
            for index, item in enumerate(self.pick_list)
            if is_mention(item)
            and not is_user_of_team_active(
                team_id=team_id, user_id=get_user_id_in_mention(item)
            )
        ]
        self.remove_items(indices_of_items_to_remove=indices_of_items_to_remove)

    def select_from_pick_list(self, *, number_of_items_to_select: int) -> list[str]:
        return [
            self.select_one_from_pick_list() for _ in range(number_of_items_to_select)
        ]

    def select_one_from_pick_list(self) -> str:
        [selected_item] = random.choices(self.pick_list, weights=self.weight_list)

        index_of_item = self.pick_list.index(selected_item)
        self.update(indices_selected=[index_of_item])
        self.remove_items(indices_of_items_to_remove=[index_of_item])
        if not len(self.pick_list):
            self.reset_lists()

        return selected_item

    def _assert_pick_list_valid_after_self_exclusion(self):
        return assert_pick_list_valid_after_self_exclusion(self.pick_list)

    def _assert_pick_list_valid_after_filtering_inactive_users(self):
        return assert_pick_list_valid_after_filtering_inactive_users(self.pick_list)

    # -------------------------------------------------------------------------
    # ----------------------- PICK LIST MANIPULATION --------------------------
    # -------------------------------------------------------------------------

    def add_items(self, items_to_add: int, new_value_weight: float = None) -> None:
        if new_value_weight is None:
            new_value_weight = 1 / len(self.weight_list)

        self.pick_list += items_to_add
        self.weight_list += [new_value_weight] * len(items_to_add)
        self.weight_list = normalize(self.weight_list)

    def remove_items(self, indices_of_items_to_remove: int) -> None:
        self.pick_list = [
            weight
            for (index, weight) in enumerate(self.pick_list)
            if index not in indices_of_items_to_remove
        ]
        self.weight_list = normalize(
            [
                weight
                for (index, weight) in enumerate(self.weight_list)
                if index not in indices_of_items_to_remove
            ]
        )

    def update(self, **kwargs) -> None:
        pass

    def reset_lists(self) -> None:
        self.pick_list = self.filtered_pick_list[:]
        self.weight_list = self.filtered_weight_list[:]

    def get_clean_lists(self) -> tuple[list[str], list[float]]:
        return self.filtered_pick_list, self.filtered_weight_list
