from argparse import ArgumentParser

from utilities.constants import LOGGER_DEBUG_ARG


def get_base_parser() -> ArgumentParser:
    """Get the base parser with the common arguments."""
    # TODO - Add `--dry-run` / `--no-dry-run`
    parser = ArgumentParser()

    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(LOGGER_DEBUG_ARG, action='store_true', help='Set logger to debug level')

    return parser
