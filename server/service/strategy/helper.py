from server.service.strategy.base import BaseStrategy
from server.service.strategy.enum import Strategy


def get_strategy(strategy_name: str, *, pick_list, weight_list=None) -> BaseStrategy:
    strategy_class = Strategy[strategy_name].value
    weight_list = (
        strategy_class.create_weight_list(len(pick_list))
        if not weight_list
        else weight_list
    )
    return strategy_class(pick_list=pick_list, weight_list=weight_list)
