from dataclasses import dataclass

from server.service.strategy.base import BaseStrategy


@dataclass
class RoundRobinStrategy(BaseStrategy):
    @staticmethod
    def create_weight_list(size: int) -> list[float]:
        weight_list = [0 for _ in range(size)]
        weight_list[0] = 1
        return weight_list

    def update(self, **kwargs) -> list[float]:
        index_selected = self.weight_list.index(1)
        next_index = (index_selected + 1) % len(self.weight_list)
        self.weight_list[index_selected] = 0
        self.weight_list[next_index] = 1
        return self.weight_list

    def add_elements(self, number_of_elements_to_add: int) -> None:
        return super().add_elements(number_of_elements_to_add, new_value_weight=0)

    def remove_elements(self, indices_of_element_to_remove: int) -> None:
        index_selected = self.weight_list.index(1)

        if index_selected in indices_of_element_to_remove:
            self.update()
            return self.remove_elements(indices_of_element_to_remove)

        return super().remove_elements(indices_of_element_to_remove)
