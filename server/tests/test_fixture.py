import random

import pytest


@pytest.fixture
def set_seed():
    random.seed(1)
