import sys
from argparse import Namespace
from typing import Final, List

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'clang_format'

ERROR_LIMIT: Final[int] = 0

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--error-limit', type=int, default=ERROR_LIMIT)

    return base_parse.parse_args()


def file_failed_check(file_name: str, error_limit: int) -> bool:
    cmd: List[str] = ['clang-format', '--style=file', '--dry-run', '-Werror', '--ferror-limit', str(error_limit), file_name]
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
        res = file_failed_check(file_name, args.error_limit)
        if not res:
            continue
        rc = 1
        logger.error('File [%s] failed %s check', file_name, HOOK_NAME)

    return rc


if __name__ == '__main__':
    sys.exit(main())
