import sys
from argparse import Namespace
from typing import Final, List, Optional, Tuple

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.models import CmdOutput
from personal_pre_commit_hooks.utilities.output_utils import output_hook_error
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'clang_format'

ERROR_LIMIT: Final[int] = 0

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--error-limit', type=int, default=ERROR_LIMIT)

    return base_parse.parse_args()


def file_failed_check(file_name: str, error_limit: int) -> Tuple[bool, Optional[str]]:
    cmd: List[str] = ['clang-format', '--style=file', '--dry-run', '-Werror', '--ferror-limit', str(error_limit), file_name]
    cmd_output: CmdOutput = wait_to_finish(run_cmd(cmd))

    if cmd_output.stderr and False:
        # FIXME - Only log error if some configuration error.
        logger.error('Failed to execute %s [%s]', HOOK_NAME, cmd_output.stderr)
        raise RuntimeError(cmd_output.stderr)
    return cmd_output.rc != 0, cmd_output.stdout


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res: bool
        hook_output: Optional[str]
        res, hook_output = file_failed_check(file_name, args.error_limit)
        if not res:
            continue
        rc = 1
        output_hook_error(hook_name=HOOK_NAME, file_name=file_name, hook_output=hook_output, hook_args=args)

    return rc


if __name__ == '__main__':
    sys.exit(main())
