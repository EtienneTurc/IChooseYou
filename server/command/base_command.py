import argparse


class BaseCommand:
    name = ""
    args = {}

    def exec(self, text):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        for arg in self.args.values():
            parser = arg.add_to_parser(parser)

        options = parser.parse_args(text.split(" "))

        return options.__dict__
