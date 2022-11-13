from dataclasses import dataclass

import numpy as np

from server.service.strategy.base import BaseStrategy


@dataclass
class RoundRobinStrategy(BaseStrategy):
    @staticmethod
    def create_weight_list(size: int) -> list[float]:
        weight_list = [0 for _ in range(size)]
        weight_list[0] = 1
        return weight_list

    def select_one_from_pick_list(self) -> str:
        index_to_select = self.weight_list.index(1)
        selected_item = self.pick_list[index_to_select]
        self.shift_selected_index()
        return selected_item

    def shift_selected_index(self) -> None:
        index_selected = self.weight_list.index(1)
        next_index = (index_selected + 1) % len(self.weight_list)
        self.weight_list = [0] * len(self.weight_list)
        self.weight_list[next_index] = 1

    # Warning: Changes the order of the pick list
    def update(self, indices_selected: int) -> None:
        current_selected_index = self.weight_list.index(1)
        new_list_order, next_selected_item_index = self.compute_new_list_order(
            current_selected_index, indices_selected
        )
        self.pick_list = list(np.array(self.pick_list)[new_list_order])
        self.weight_list = [0] * len(self.weight_list)
        self.weight_list[next_selected_item_index] = 1

    def compute_new_list_order(
        self, current_selected_index, indices_selected: int
    ) -> tuple[list[int], int]:
        shifted_selected_indices = (
            np.array(indices_selected) - current_selected_index
        ) % len(self.pick_list)
        uniq_shifted_selected_indices = shifted_selected_indices[
            : list(shifted_selected_indices).index(max(shifted_selected_indices)) + 1
        ]  # Assumes that shifted_selected_indices are in increasing order

        shifted_unselected_indices = np.array(
            [
                index
                for index in range(len(self.pick_list))
                if index not in uniq_shifted_selected_indices
            ]
        )

        uniq_selected_indices = (
            uniq_shifted_selected_indices + current_selected_index
        ) % len(self.pick_list)
        unselected_indices = (
            shifted_unselected_indices + current_selected_index
        ) % len(self.pick_list)

        return (
            list(uniq_selected_indices) + list(unselected_indices),
            len(uniq_selected_indices) % len(self.pick_list),
        )

    def add_items(self, number_of_items_to_add: int) -> None:
        return super().add_items(number_of_items_to_add, new_value_weight=0)

    def remove_items(self, indices_of_items_to_remove: int) -> None:
        if len(self.pick_list) == len(indices_of_items_to_remove):
            self.pick_list, self.weight_list = [], []
            return

        index_selected = self.weight_list.index(1)

        if index_selected in indices_of_items_to_remove:
            self.shift_selected_index()
            return self.remove_items(indices_of_items_to_remove)

        return super().remove_items(indices_of_items_to_remove)
