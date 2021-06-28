from dataclasses import dataclass

import numpy as np

from server.service.strategy.base import BaseStrategy


def reset_function(n):
    return 1 / (2 ** n)


@dataclass
class SmoothStrategy(BaseStrategy):
    def update(self, *, index_selected: int, **kwargs) -> list[float]:
        reset_value = reset_function(len(self.weight_list))
        self.weight_list[index_selected] = reset_value
        self.weight_list = list(np.array(self.weight_list) / np.sum(self.weight_list))
        return self.weight_list
