from server.service.strategy.base import BaseStrategy
from server.service.strategy.enum import Strategy


def get_strategy(strategy_name: str, weight_list=None, size=None) -> BaseStrategy:
    strategy_class = Strategy[strategy_name].value
    weight_list = (
        strategy_class.create_weight_list(size) if not weight_list else weight_list
    )
    return strategy_class(weight_list=weight_list)
