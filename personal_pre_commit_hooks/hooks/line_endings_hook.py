import re
import sys
from argparse import Namespace
from typing import Final, List, Optional, Tuple, cast

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.models import CmdOutput
from personal_pre_commit_hooks.utilities.output_utils import output_hook_error
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'line_endings'

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    return base_parse.parse_args()


def file_failed_check(file_name) -> Tuple[bool, Optional[str]]:
    cmd: List[str] = ['file', file_name]
    cmd_output: CmdOutput = wait_to_finish(run_cmd(cmd))

    if (cmd_output.stderr or not cmd_output.stdout) and False:
        # FIXME - Only log error if some configuration error.
        logger.error('Failed to execute %s [%s]', HOOK_NAME, cmd_output.stderr)
        raise RuntimeError(cmd_output.stderr)

    output: Optional[str] = None
    failed: bool = False
    matched = re.search(r'with ([^ ]+) line terminators', cast(str, cmd_output.stdout))
    if matched is not None:
        failed = True
        output = f'{matched.group(1)} line endings'

    return failed, output


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res: bool
        hook_output: Optional[str]
        res, hook_output = file_failed_check(file_name)
        if not res:
            continue
        rc = 1
        output_hook_error(hook_name=HOOK_NAME, file_name=file_name, hook_output=hook_output, hook_args=args)

    return rc


if __name__ == '__main__':
    sys.exit(main())
