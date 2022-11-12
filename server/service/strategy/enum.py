from enum import Enum

from server.service.strategy.round_robin import RoundRobinStrategy
from server.service.strategy.smooth import SmoothStrategy
from server.service.strategy.uniform import UniformStrategy


class Strategy(Enum):
    smooth = SmoothStrategy
    uniform = UniformStrategy
    round_robin = RoundRobinStrategy
