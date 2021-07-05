from dataclasses import dataclass

from server.service.helper.dict_helper import normalize
from server.service.strategy.base import BaseStrategy


def reset_function(n):
    return 1 / (2 ** n)


@dataclass
class SmoothStrategy(BaseStrategy):
    def update(self, *, indices_selected: list[int], **kwargs) -> list[float]:
        reset_value = reset_function(len(self.weight_list))
        for index_selected in indices_selected:
            self.weight_list[index_selected] = reset_value
        self.weight_list = normalize(self.weight_list)
        return self.weight_list
