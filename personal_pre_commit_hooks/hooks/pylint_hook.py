import re
import sys
from argparse import Namespace
from typing import Final, List, Optional, cast

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.constants import get_config_file_path
from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.models import CmdOutput, FileCheckResult
from personal_pre_commit_hooks.utilities.output_utils import output_hook_error
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'pylint'
DEFAULT_RC_FILE: Final[str] = get_config_file_path('pylintrc')
DEFAULT_FAIL_UNDER: Final[float] = 9

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--rcfile', type=str, default=DEFAULT_RC_FILE)
    base_parse.add_argument('--fail-under', type=int, default=DEFAULT_FAIL_UNDER, choices=list(range(11)))

    return base_parse.parse_args()


def file_failed_check(file_name: str, rcfile: str, fail_under: float) -> FileCheckResult:
    cmd: List[str] = ['pylint', file_name, '--rcfile', rcfile, '--fail-under', str(fail_under)]
    cmd_output: CmdOutput = wait_to_finish(run_cmd(cmd))

    if cmd_output.stderr and False:
        # FIXME - Only log error if some configuration error.
        logger.error('Failed to execute %s [%s]', HOOK_NAME, cmd_output.stderr)
        raise RuntimeError(cmd_output.stderr)

    output: Optional[str] = None
    if cmd_output.rc != 0:
        proc_stdout_lines = cast(str, cmd_output.stdout).split('\n')
        logger.debug('%s output:\n%s', HOOK_NAME, cmd_output.stdout)
        output = ', '.join(line for line in proc_stdout_lines if re.match(r'^Your code has been rated.*', line))

    return FileCheckResult(file_name=file_name, failed=cmd_output.rc != 0, cmd=cmd, hook_output=output)


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res: FileCheckResult = file_failed_check(file_name, args.rcfile, args.fail_under)
        if not res.failed:
            continue
        rc = 1
        output_hook_error(hook_name=HOOK_NAME, hook_result=res, hook_args=args)

    return rc


if __name__ == '__main__':
    sys.exit(main())
