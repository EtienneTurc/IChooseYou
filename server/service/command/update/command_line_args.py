from server.service.command_line.arg import Arg

POSITIONAL_ARG = [
    Arg(
        name="command_to_update",
        prefix="",
        nargs=1,
    ),
]

NAMED_ARGS = [
    Arg(name="label", short="l", nargs="*"),
    Arg(
        name="pick-list",
        short="p",
        nargs="*",
        type=list,
        clean_mentions=True,
    ),
    Arg(
        name="add-to-pick-list",
        short="a",
        nargs="*",
        type=list,
        clean_mentions=True,
    ),
    Arg(
        name="remove-from-pick-list",
        short="r",
        nargs="*",
        type=list,
        clean_mentions=True,
    ),
    Arg(
        name="strategy",
        short="s",
        nargs="*",
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
