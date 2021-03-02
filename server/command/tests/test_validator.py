import pytest

from server.command.args import ArgError
from server.command.validator import assert_label_is_correct


@pytest.mark.parametrize(
    "label, expected_not_to_raise",
    [
        ("$1", True),
        ("$2", False),
        ("$1 $1", True),
        ("$1 $3", False),
        ("$name", True),
        ("$name $name", True),
        ("$name $dollar", True),
        ("$1 and $name $dollar", True),
    ],
)
def test_assert_label_is_correct(label, expected_not_to_raise):
    if not expected_not_to_raise:
        with pytest.raises(ArgError):
            assert_label_is_correct(label)
    else:
        assert_label_is_correct(label)
