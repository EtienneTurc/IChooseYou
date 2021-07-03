from dataclasses import dataclass

import numpy as np

from server.service.error.back_error import BackError


@dataclass
class BaseStrategy:
    weight_list: list[float]

    @staticmethod
    def create_weight_list(size: int) -> list[float]:
        return [1 / size for _ in range(size)]

    def __post_init__(self) -> None:
        if not self.weight_list or not len(self.weight_list):
            raise BackError("Weight list must not be empty.", 400)

        if not self.validate():
            raise BackError("Weight list must sum up to 1.", 400)

    def validate(self) -> bool:
        return np.sum(self.weight_list) == 1

    def add_elements(
        self, number_of_elements_to_add: int, new_value_weight: float = None
    ) -> None:
        if new_value_weight is None:
            new_value_weight = 1 / len(self.weight_list)

        self.weight_list += [new_value_weight] * number_of_elements_to_add
        self.weight_list = list(np.array(self.weight_list) / np.sum(self.weight_list))

    def remove_elements(self, indices_of_elements_to_remove: int) -> None:
        self.weight_list = np.array(
            [
                weight
                for (index, weight) in enumerate(self.weight_list)
                if index not in indices_of_elements_to_remove
            ]
        )
        self.weight_list = list(self.weight_list / np.sum(self.weight_list))

    def update(self, **kwargs) -> list[float]:
        return self.weight_list