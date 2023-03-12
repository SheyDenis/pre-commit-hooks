import sys
from argparse import Namespace
from typing import Final, List

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.constants import get_config_file_path
from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'isort'
DEFAULT_SETTINGS_FILE: Final[str] = get_config_file_path('isort.cfg')

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--settings-file', type=str, default=DEFAULT_SETTINGS_FILE)

    return base_parse.parse_args()


def file_failed_check(file_name: str, settings_file: str) -> bool:
    cmd: List[str] = ['isort', '--quiet', '--check-only', file_name, '--settings-file', settings_file]
    proc_rc, _, proc_stderr = wait_to_finish(run_cmd(cmd))

    if proc_stderr and False:
        # FIXME - Only log error if some configuration error.
        logger.error('Failed to execute %s [%s]', HOOK_NAME, proc_stderr)
        raise RuntimeError(proc_stderr)

    return proc_rc != 0


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res = file_failed_check(file_name, args.settings_file)
        if not res:
            continue
        rc = 1
        logger.error('File [%s] failed %s check', file_name, HOOK_NAME)

    return rc


if __name__ == '__main__':
    sys.exit(main())
