from dataclasses import dataclass

from server.service.strategy.base import BaseStrategy


@dataclass
class UniformStrategy(BaseStrategy):
    def update(self, **kwargs) -> list[float]:
        return self.weight_list
