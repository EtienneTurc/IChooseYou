from server.service.strategy.uniform import UniformStrategy


def test_uniform_update():
    weight_list = [1 / 3, 2 / 3]
    result = UniformStrategy(weight_list=weight_list).update()
    assert result == weight_list
