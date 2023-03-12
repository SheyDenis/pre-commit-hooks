import os
import sys
from argparse import Namespace
from typing import Final, List

from utilities.argparse import get_base_parser
from utilities.logger import global_logger as logger
from utilities.proc import run_cmd, wait_to_finish

__CURRENT_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SETTINGS_FILE: Final[str] = os.path.normpath(os.path.join(__CURRENT_DIR, os.path.pardir, 'configs', 'isort.cfg'))

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--settings-file', type=str, default=DEFAULT_SETTINGS_FILE)

    return base_parse.parse_args()


def file_failed_check(file_name: str, settings_file: str) -> bool:
    cmd: List[str] = ['isort', '--quiet', '--check-only', file_name, '--settings-file', settings_file]
    proc_rc, _, _ = wait_to_finish(run_cmd(cmd))

    return proc_rc != 0


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res = file_failed_check(file_name, args.settings_file)
        if not res:
            continue
        rc = 1
        logger.error('File [%s] failed isort check', file_name)

    return rc


if __name__ == '__main__':
    sys.exit(main())
