from argparse import ArgumentParser

from personal_pre_commit_hooks.utilities.constants import LOGGER_DEBUG_ARG


def get_base_parser(**kwargs) -> ArgumentParser:
    """Get the base parser with the common arguments."""
    parser = ArgumentParser(**kwargs)

    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(LOGGER_DEBUG_ARG, action='store_true', help='Set logger to debug level')
    parser.add_argument('--quiet', action='store_true', help='Only output if a hook failed or not without detailed output')

    dry_run_group = parser.add_mutually_exclusive_group()
    dry_run_group.add_argument('--dry-run', action='store_true', dest='dry_run', default=True)
    dry_run_group.add_argument('--no-dry-run', action='store_false', dest='dry_run')

    return parser
