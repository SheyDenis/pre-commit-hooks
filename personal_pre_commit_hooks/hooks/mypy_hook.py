import sys
from argparse import Namespace
from typing import Final, List

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.models import CmdOutput, FileCheckResult
from personal_pre_commit_hooks.utilities.output_utils import output_hook_error
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

# pylint: disable=missing-function-docstring
HOOK_NAME: Final[str] = 'mypy'


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()
    return base_parse.parse_args()


def file_failed_check(file_name: str) -> FileCheckResult:
    cmd: List[str] = [
        'mypy',
        '--follow-imports=silent',
        '--ignore-missing-imports',
        file_name,
    ]
    cmd_output: CmdOutput = wait_to_finish(run_cmd(cmd))

    return FileCheckResult(file_name=file_name, failed=cmd_output.rc != 0, cmd=cmd, hook_output=cmd_output.stdout)


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res: FileCheckResult = file_failed_check(file_name)
        if not res.failed:
            continue
        rc = 1
        output_hook_error(hook_name=HOOK_NAME, hook_result=res, hook_args=args)

    return rc


if __name__ == '__main__':
    sys.exit(main())
