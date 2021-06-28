from enum import Enum

from server.service.strategy.round_robin import RoundRobinStrategy
from server.service.strategy.smooth import SmoothStrategy
from server.service.strategy.uniform import UniformStrategy


class Strategy(Enum):
    uniform = UniformStrategy
    smooth = SmoothStrategy
    round_robin = RoundRobinStrategy
