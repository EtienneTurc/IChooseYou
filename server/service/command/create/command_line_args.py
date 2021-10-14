from server.service.command_line.arg import Arg

POSITIONAL_ARG = [
    Arg(
        name="new_command_name",
        prefix="",
        nargs=1,
    ),
]

NAMED_ARGS = [
    Arg(name="label", short="l", nargs="+"),
    Arg(name="description", short="d", nargs="+"),
    Arg(
        name="pick-list",
        short="p",
        nargs="+",
        clean_mentions=True,
        type=list,
    ),
    Arg(
        name="strategy",
        short="s",
        nargs="?",
    ),
    Arg(
        name="self-exclude",
        short="e",
        nargs="?",
        const="True",
        type=bool,
    ),
    Arg(
        name="only-active-users",
        short="o",
        nargs="?",
        const="True",
        type=bool,
    ),
]
