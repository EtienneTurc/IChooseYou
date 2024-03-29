from server.service.command_line.arg import Arg

POSITIONAL_ARG = []

NAMED_ARGS = [
    Arg(
        name="number-of-items-to-select",
        short="n",
        nargs="?",
        type=int,
    ),
    Arg(
        name="with-wheel",
        short="w",
        nargs="?",
        const="True",
        type=bool,
    ),
]
