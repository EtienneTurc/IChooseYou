from dataclasses import dataclass

from server.service.strategy.base import BaseStrategy


@dataclass
class RoundRobinStrategy(BaseStrategy):
    @staticmethod
    def create_weight_list(size: int) -> list[float]:
        weight_list = [0 for _ in range(size)]
        weight_list[0] = 1
        return weight_list

    def update(self, *, indices_selected, **kwargs) -> list[float]:
        last_index_selected = indices_selected[-1]
        next_index = (last_index_selected + 1) % len(self.weight_list)
        self.weight_list = [0] * len(self.weight_list)
        self.weight_list[next_index] = 1
        return self.weight_list

    def add_items(self, number_of_items_to_add: int) -> None:
        return super().add_items(number_of_items_to_add, new_value_weight=0)

    def remove_items(self, indices_of_item_to_remove: int) -> None:
        index_selected = self.weight_list.index(1)

        if index_selected in indices_of_item_to_remove:
            self.update(indices_selected=[index_selected])
            return self.remove_items(indices_of_item_to_remove)

        return super().remove_items(indices_of_item_to_remove)
