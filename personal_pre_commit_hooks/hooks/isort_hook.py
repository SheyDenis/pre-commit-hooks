import sys
from argparse import Namespace
from typing import Final, List, Optional, Tuple

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.constants import get_config_file_path
from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.models import CmdOutput
from personal_pre_commit_hooks.utilities.output_utils import output_hook_error
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'isort'
DEFAULT_SETTINGS_FILE: Final[str] = get_config_file_path('isort.cfg')

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--settings-file', type=str, default=DEFAULT_SETTINGS_FILE)
    base_parse.add_argument('--fix', action='store_true', help='Fix for failed files.')

    return base_parse.parse_args()


def file_failed_check(file_name: str, settings_file: str, fix: bool) -> Tuple[bool, Optional[str]]:
    cmd: List[str] = ['isort', '--check-only' if not fix else '', file_name, '--settings-file', settings_file, '--src', '.']
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
        res, hook_output = file_failed_check(file_name, args.settings_file, False)
        if not res:
            continue

        rc = 1
        output_hook_error(hook_name=HOOK_NAME, file_name=file_name, hook_output=hook_output, hook_args=args)
        if args.fix:
            _, _ = file_failed_check(file_name, args.settings_file, args.fix)

    return rc


if __name__ == '__main__':
    sys.exit(main())
