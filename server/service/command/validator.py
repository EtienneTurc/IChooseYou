from server.service.command.args import ArgError
from server.service.command.utils import get_args_in_label


def assert_label_is_correct(label):
    positional_args, _ = get_args_in_label(label)

    pos_args = {}
    for arg in positional_args:
        value = int(arg[1:])
        if value < 1:
            raise ArgError(
                None, "Positional args in label must start from 1, ex: $1 $2 etc."
            )
        pos_args[value] = True

    positions = pos_args.keys()
    if not positions:
        return

    n = len(positions)
    if max(positions) != n:
        raise ArgError(None, "Positional args in label must be consecutive.")

    return


def assert_positional_args(req_positional_args, label_positional_args):
    diff = len(req_positional_args) - len(set(label_positional_args))
    if diff < 0:
        raise ArgError(None, f"Missing {-diff} positional arguments.")
    elif diff > 0:
        raise ArgError(None, f"Too many positional arguments ({diff}).")


def assert_named_args(req_named_args, label_named_args):
    req_named_args_set = set([arg.name for arg in req_named_args])
    label_named_args_set = set([arg[1:] for arg in label_named_args])

    missing = req_named_args_set - label_named_args_set
    if len(missing):
        raise ArgError(None, f"Missing named args: {list(missing)}.")

    too_many = label_named_args_set - req_named_args_set
    if len(too_many):
        raise ArgError(
            None, f"Too many named args ({len(too_many)}): {list(too_many)}."
        )
