from argparse import ArgumentParser

from server.service.command_line.arg import Arg
from server.service.command_line.clean_parser_output import (clean_empty_fields,
                                                             options_to_dict)


def parse_command_line(
    text: str, expected_positional_args: list[Arg], expected_named_args: list[Arg]
) -> dict[str, any]:
    if text is None:
        return {}

    text_as_list = format_text_to_list(text)
    positional_args, named_arg = separate_positional_and_named_args(text_as_list)

    values = clean_empty_fields(
        {
            **parse_positional_args(positional_args, expected_positional_args),
            **parse_named_args(named_arg, expected_named_args),
        }
    )

    return {
        **values,
        "additional_text": extract_additional_text(
            positional_args[len(expected_positional_args):] + named_arg,
            expected_named_args,
            values,
        ),
    }


def format_text_to_list(text: str) -> list[str]:
    text = text.lstrip()
    text_list = []
    if text:
        text_list = text.split(" ")
    return text_list


def separate_positional_and_named_args(
    text_as_list: list[str],
) -> tuple[list[str], list[str]]:
    for index, word in enumerate(text_as_list):
        if word.startswith("-"):
            return text_as_list[:index], text_as_list[index:]

    return text_as_list, []


def parse_positional_args(
    positional_args: list[str], expected_positional_args: list[Arg]
) -> dict[str, any]:
    options = {
        expected_positional_args[i].name: positional_args[i]
        for i in range(min(len(positional_args), len(expected_positional_args)))
    }

    return options_to_dict(options, expected_positional_args)


def parse_named_args(
    named_arg: list[str], expected_named_args: list[Arg]
) -> dict[str, any]:
    parser = create_named_arg_parser(expected_named_args)
    options, _ = parser.parse_known_args(named_arg)

    parsed_named_args = options_to_dict(options.__dict__, expected_named_args)
    for arg in expected_named_args:
        if arg.type is bool and parsed_named_args.get(arg.variable_name):
            parsed_named_args[arg.variable_name] = True
    return parsed_named_args


def create_named_arg_parser(
    expected_named_args: list[Arg],
):
    parser = ArgumentParser(exit_on_error=False, add_help=False)
    for arg in expected_named_args:
        arg.add_to_parser(parser)
    return parser


def extract_additional_text(
    text_as_list: list[str], expected_named_args: list[Arg], values: dict[str, any]
) -> str:
    additional_text = " ".join(text_as_list)
    for arg in expected_named_args:
        if values.get(arg.variable_name):
            additional_text = additional_text.replace(
                f"{arg.prefix}{arg.name} {values.get(arg.variable_name)}",
                "",
            )
            additional_text = additional_text.replace(
                f"-{arg.short} {values.get(arg.variable_name)}", ""
            )

            if arg.type is bool:
                additional_text = additional_text.replace(f"{arg.prefix}{arg.name}", "")
                additional_text = additional_text.replace(f"-{arg.short}", "")

            additional_text = additional_text.strip()
            additional_text = additional_text.replace("  ", " ")
    return additional_text
