from server.service.command_line.arg import Arg

POSITIONAL_ARG = []

NAMED_ARGS = [
    Arg(name="label", short="l", nargs="+"),
    Arg(
        name="pick-list",
        short="p",
        nargs="+",
        clean_mentions=True,
        type=list,
    ),
    Arg(
        name="number-of-items-to-select",
        short="n",
        nargs="?",
        type=int,
    ),
    Arg(
        name="only-active-users",
        short="o",
        nargs="?",
        const="True",
        type=bool,
    ),
]
